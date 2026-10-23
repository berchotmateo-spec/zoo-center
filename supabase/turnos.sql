-- =====================================================================
--  Zoo Center · agenda de turnos (que dos clientes no pidan el mismo horario)
-- ---------------------------------------------------------------------
--  Se pega ENTERO en Supabase → SQL Editor → Run. Se puede volver a
--  correr: no borra turnos, solo actualiza las funciones.
--
--  Después, en una consulta aparte (que NO se guarda en el repo):
--      select public.fijar_clave('acá-la-clave-del-local');
--  Es la "clave del local" (8 caracteres o más) que el dueño escribe una
--  vez en su celular para ver la agenda y confirmar turnos.
--
--  Cómo se protege:
--  - La página usa solo la clave PUBLICABLE de Supabase y nunca toca la
--    tabla directo (RLS activado y sin políticas): todo pasa por estas
--    funciones.
--  - Cualquiera puede ver QUÉ horarios están ocupados, pero no de quién.
--  - Nombres y teléfonos solo se leen con la clave del local.
--  - Un pedido de la web reserva su horario 24 horas; si el local no lo
--    confirma, se libera solo (por si el cliente nunca mandó el WhatsApp).
-- =====================================================================

create extension if not exists pgcrypto with schema extensions;

create table if not exists public.turnos (
  id        uuid primary key default gen_random_uuid(),
  tipo      text not null check (tipo in ('vet', 'pelu')),
  fecha     date not null,
  hora      time not null,
  duracion  int  not null check (duracion between 10 and 240),     -- minutos
  estado    text not null default 'pedido' check (estado in ('pedido', 'confirmado', 'liberado')),
  origen    text not null default 'web' check (origen in ('web', 'local')),
  nombre    text not null default '' check (char_length(nombre) <= 60),
  whatsapp  text not null default '' check (whatsapp = '' or whatsapp ~ '^549[0-9]{10}$'),
  detalle   text not null default '' check (char_length(detalle) <= 400),
  creado    timestamptz not null default now()
);
create index if not exists turnos_dia on public.turnos (tipo, fecha);
alter table public.turnos enable row level security;    -- sin políticas: nadie entra directo

create table if not exists public.ajustes (
  nombre text primary key,
  valor  text not null
);
alter table public.ajustes enable row level security;

drop function if exists public.horarios_ocupados(date, date);
drop function if exists public.reservar_turno(text, date, time, int, text, text, text);
drop function if exists public.agenda(text, date, date);
drop function if exists public.cambiar_turno(text, uuid, text, date, time);
drop function if exists public.ocupar_horario(text, text, date, time, int, text);
drop function if exists public.choca(text, date, time, int, uuid);
drop function if exists public.turno_vigente(public.turnos);
drop function if exists public.clave_ok(text);
drop function if exists public.hoy_ar();

-- Hoy, en hora de Argentina (Supabase trabaja en UTC).
create function public.hoy_ar() returns date
language sql stable set search_path = '' as $$
  select (now() at time zone 'America/Argentina/Buenos_Aires')::date
$$;

-- Un turno ocupa su horario si está confirmado, o si es un pedido de hace menos de 24 horas.
create function public.turno_vigente(t public.turnos) returns boolean
language sql stable set search_path = '' as $$
  select t.estado = 'confirmado' or (t.estado = 'pedido' and t.creado > now() - interval '24 hours')
$$;

-- ¿Ese horario se pisa con otro turno vigente del mismo tipo? (p_menos: no contar este turno)
create function public.choca(p_tipo text, p_fecha date, p_hora time, p_duracion int, p_menos uuid default null)
returns boolean language sql stable set search_path = '' as $$
  select exists (
    select 1 from public.turnos t
    where t.tipo = p_tipo and t.fecha = p_fecha and public.turno_vigente(t)
      and (p_menos is null or t.id <> p_menos)
      and extract(epoch from t.hora) / 60 < extract(epoch from p_hora) / 60 + p_duracion
      and extract(epoch from p_hora) / 60 < extract(epoch from t.hora) / 60 + t.duracion
  )
$$;

create function public.clave_ok(p_clave text) returns void
language plpgsql security definer set search_path = '' as $$
declare h text;
begin
  select valor into h from public.ajustes where nombre = 'clave';
  if h is null or p_clave is null or extensions.crypt(p_clave, h) <> h then
    perform pg_sleep(1);                         -- frena a quien quiera adivinarla
    raise exception 'clave';
  end if;
end $$;

-- Solo desde el SQL Editor de Supabase (la página no puede llamarla).
create or replace function public.fijar_clave(p_nueva text) returns text
language plpgsql security definer set search_path = '' as $$
begin
  if char_length(coalesce(p_nueva, '')) < 8 then
    raise exception 'La clave tiene que tener 8 caracteres o más';
  end if;
  insert into public.ajustes (nombre, valor) values ('clave', extensions.crypt(p_nueva, extensions.gen_salt('bf')))
  on conflict (nombre) do update set valor = excluded.valor;
  return 'Clave del local guardada';
end $$;

-- ---------- lo que usa el formulario de turnos (sin clave) ----------

-- Horarios ocupados (sin datos de nadie), de hoy en adelante.
create function public.horarios_ocupados(p_desde date, p_hasta date)
returns table (tipo text, fecha date, hora time, duracion int)
language sql stable security definer set search_path = '' as $$
  select t.tipo, t.fecha, t.hora, t.duracion
  from public.turnos t
  where t.fecha between greatest(p_desde, public.hoy_ar()) and least(p_hasta, p_desde + 92)
    and public.turno_vigente(t)
  order by t.fecha, t.hora
$$;

-- Reserva un horario si está libre. Errores: 'ocupado', 'fecha', 'demasiados'.
create function public.reservar_turno(p_tipo text, p_fecha date, p_hora time, p_duracion int,
                                      p_nombre text, p_whatsapp text, p_detalle text default '')
returns uuid language plpgsql security definer set search_path = '' as $$
declare nuevo uuid;
begin
  if p_fecha < public.hoy_ar() or p_fecha > public.hoy_ar() + 92 then
    raise exception 'fecha';
  end if;
  -- freno a abusos: 40 pedidos por hora en total y 3 turnos vigentes por número
  if (select count(*) from public.turnos where origen = 'web' and creado > now() - interval '1 hour') >= 40
     or (select count(*) from public.turnos t
         where t.whatsapp = p_whatsapp and t.fecha >= public.hoy_ar() and public.turno_vigente(t)) >= 3 then
    raise exception 'demasiados';
  end if;
  perform pg_advisory_xact_lock(hashtext('turnos ' || p_tipo || ' ' || p_fecha));   -- de a uno por día y tipo
  if public.choca(p_tipo, p_fecha, p_hora, p_duracion) then
    raise exception 'ocupado';
  end if;
  insert into public.turnos (tipo, fecha, hora, duracion, nombre, whatsapp, detalle)
  values (p_tipo, p_fecha, p_hora, p_duracion, left(coalesce(p_nombre, ''), 60), p_whatsapp, left(coalesce(p_detalle, ''), 400))
  returning id into nuevo;
  return nuevo;
end $$;

-- ---------- lo que usa el dueño (con la clave del local) ----------

create function public.agenda(p_clave text, p_desde date, p_hasta date)
returns table (id uuid, tipo text, fecha date, hora time, duracion int, estado text, origen text,
               nombre text, whatsapp text, detalle text, creado timestamptz, vigente boolean)
language plpgsql security definer set search_path = '' as $$
#variable_conflict use_column
begin
  perform public.clave_ok(p_clave);
  return query
    select t.id, t.tipo, t.fecha, t.hora, t.duracion, t.estado, t.origen, t.nombre, t.whatsapp, t.detalle,
           t.creado, public.turno_vigente(t)
    from public.turnos t
    where t.fecha between p_desde and least(p_hasta, p_desde + 92) and t.estado <> 'liberado'
    order by t.fecha, t.hora;
end $$;

-- Confirmar, liberar o pasar a otro horario (p_fecha y p_hora, queda confirmado).
create function public.cambiar_turno(p_clave text, p_id uuid, p_estado text,
                                     p_fecha date default null, p_hora time default null)
returns text language plpgsql security definer set search_path = '' as $$
declare t public.turnos;
begin
  perform public.clave_ok(p_clave);
  if p_estado not in ('confirmado', 'liberado') then
    raise exception 'estado';
  end if;
  select * into t from public.turnos where id = p_id for update;
  if not found then
    raise exception 'no existe';
  end if;
  if p_estado = 'liberado' then
    update public.turnos set estado = 'liberado' where id = p_id;
  elsif p_fecha is not null and p_hora is not null then
    perform pg_advisory_xact_lock(hashtext('turnos ' || t.tipo || ' ' || p_fecha));
    if public.choca(t.tipo, p_fecha, p_hora, t.duracion, t.id) then
      raise exception 'ocupado';
    end if;
    update public.turnos set fecha = p_fecha, hora = p_hora, estado = 'confirmado' where id = p_id;
  else
    if not public.turno_vigente(t) then        -- venció: solo si nadie tomó el horario mientras tanto
      perform pg_advisory_xact_lock(hashtext('turnos ' || t.tipo || ' ' || t.fecha));
      if public.choca(t.tipo, t.fecha, t.hora, t.duracion, t.id) then
        raise exception 'ocupado';
      end if;
    end if;
    update public.turnos set estado = 'confirmado' where id = p_id;
  end if;
  return p_estado;
end $$;

-- Turnos que dan por teléfono o en el local, para que la web no ofrezca ese horario.
create function public.ocupar_horario(p_clave text, p_tipo text, p_fecha date, p_hora time,
                                      p_duracion int, p_nota text default '')
returns uuid language plpgsql security definer set search_path = '' as $$
declare nuevo uuid;
begin
  perform public.clave_ok(p_clave);
  perform pg_advisory_xact_lock(hashtext('turnos ' || p_tipo || ' ' || p_fecha));
  if public.choca(p_tipo, p_fecha, p_hora, p_duracion) then
    raise exception 'ocupado';
  end if;
  insert into public.turnos (tipo, fecha, hora, duracion, estado, origen, nombre)
  values (p_tipo, p_fecha, p_hora, p_duracion, 'confirmado', 'local', left(coalesce(p_nota, ''), 60))
  returning id into nuevo;
  return nuevo;
end $$;

-- ---------- permisos: la página solo ve estas cinco funciones ----------
revoke all on table public.turnos, public.ajustes from anon, authenticated;
revoke all on function public.hoy_ar(), public.turno_vigente(public.turnos),
  public.choca(text, date, time, int, uuid), public.clave_ok(text), public.fijar_clave(text)
  from public, anon, authenticated;
revoke all on function public.horarios_ocupados(date, date),
  public.reservar_turno(text, date, time, int, text, text, text), public.agenda(text, date, date),
  public.cambiar_turno(text, uuid, text, date, time), public.ocupar_horario(text, text, date, time, int, text)
  from public;
grant execute on function public.horarios_ocupados(date, date),
  public.reservar_turno(text, date, time, int, text, text, text), public.agenda(text, date, date),
  public.cambiar_turno(text, uuid, text, date, time), public.ocupar_horario(text, text, date, time, int, text)
  to anon, authenticated;
