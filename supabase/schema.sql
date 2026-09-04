create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  username text unique,
  display_name text,
  role text not null default 'user2' check (role in ('admin','user2','user3')),
  legacy_kind text,
  created_at timestamptz not null default now()
);

create table if not exists public.customers (
  code text primary key,
  name text not null,
  city text,
  address text,
  phone text,
  updated_at timestamptz not null default now()
);

create table if not exists public.products (
  code text primary key,
  name text not null,
  user2_price numeric(14,2) not null default 0,
  user3_price numeric(14,2) not null default 0,
  updated_at timestamptz not null default now()
);

create table if not exists public.invoices (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete restrict,
  local_number text not null,
  customer_code text,
  customer_name text,
  city text,
  seller text,
  section text,
  package_type text,
  package_count numeric(12,2) not null default 0,
  price_mode text not null check (price_mode in ('user2','user3')),
  total_qty numeric(14,2) not null default 0,
  total_amount numeric(14,2) not null default 0,
  created_at timestamptz not null default now(),
  unique(owner_id, local_number)
);

create table if not exists public.invoice_items (
  id uuid primary key default gen_random_uuid(),
  invoice_id uuid not null references public.invoices(id) on delete cascade,
  product_code text not null,
  product_name text not null,
  unit_price numeric(14,2) not null default 0,
  quantity numeric(14,2) not null default 0,
  total numeric(14,2) not null default 0
);

alter table public.profiles enable row level security;
alter table public.customers enable row level security;
alter table public.products enable row level security;
alter table public.invoices enable row level security;
alter table public.invoice_items enable row level security;

create policy "profiles self read" on public.profiles for select using (id = auth.uid());
create policy "catalog authenticated read" on public.customers for select to authenticated using (true);
create policy "products authenticated read" on public.products for select to authenticated using (true);
create policy "invoice owner read" on public.invoices for select using (owner_id = auth.uid());
create policy "invoice owner insert" on public.invoices for insert with check (owner_id = auth.uid());
create policy "invoice owner update" on public.invoices for update using (owner_id = auth.uid()) with check (owner_id = auth.uid());
create policy "invoice owner items read" on public.invoice_items for select using (exists (select 1 from public.invoices i where i.id = invoice_id and i.owner_id = auth.uid()));
create policy "invoice owner items insert" on public.invoice_items for insert with check (exists (select 1 from public.invoices i where i.id = invoice_id and i.owner_id = auth.uid()));

create or replace function public.handle_new_user() returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, username, display_name) values (new.id, coalesce(new.raw_user_meta_data->>'username', new.email), coalesce(new.raw_user_meta_data->>'display_name', new.email));
  return new;
end; $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute procedure public.handle_new_user();
