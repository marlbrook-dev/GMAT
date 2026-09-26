-- Lightweight partner/outreach CRM. Admin-only via is_admin() RLS;
-- used for tutors, partner programs, communities, and affiliates.
create table if not exists crm_contacts (
  id bigserial primary key,
  name text not null,
  org text,
  type text not null default 'partner' check (type in ('tutor','partner','community','affiliate','school','other')),
  email text, phone text, url text,
  stage text not null default 'lead' check (stage in ('lead','contacted','in_talks','agreed','active','passed')),
  value_note text,
  next_action text,
  next_action_date date,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
create index if not exists crm_contacts_stage on crm_contacts(stage);
create table if not exists crm_notes (
  id bigserial primary key,
  contact_id bigint not null references crm_contacts(id) on delete cascade,
  note text not null,
  ts timestamptz default now()
);
create index if not exists crm_notes_contact on crm_notes(contact_id, ts desc);
alter table crm_contacts enable row level security;
alter table crm_notes enable row level security;
drop policy if exists "admin all contacts" on crm_contacts;
create policy "admin all contacts" on crm_contacts for all using (is_admin()) with check (is_admin());
drop policy if exists "admin all notes" on crm_notes;
create policy "admin all notes" on crm_notes for all using (is_admin()) with check (is_admin());
grant usage, select on sequence crm_contacts_id_seq, crm_notes_id_seq to authenticated;
grant select, insert, update, delete on crm_contacts, crm_notes to authenticated;
