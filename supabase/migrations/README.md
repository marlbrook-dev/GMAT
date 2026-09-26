# Migrations

Two kinds of file live here, and the difference matters when you read them.

**Exact mirrors**, named `<version>_<name>.sql` with a 14 digit version. These are the
SQL the database actually ran, pulled from `supabase_migrations.schema_migrations`. Each
one was verified by comparing its md5 against the database rather than by reading it
over, so a mirror either matches byte for byte or it was not committed.

**Annotated sources**, named `<date>_<name>.sql` with an 8 digit date. These are the
hand written originals, carrying the reasoning behind each change. The DDL is the same
statements; Supabase stores the executed form with comments stripped, so their md5 will
never match a mirror and that is expected, not drift.

Where both exist for one change, the annotated file is the better read and the mirror is
the ground truth.

## State on 2026-09-21

34 migrations are applied to project `ftsqwbzhkzuudogkvoqa`. 17 are mirrored here. The
rest are listed below with their checksums so the gap is explicit rather than implied.

Ten of the unmirrored ones already have an annotated source in this directory under a
different name, so the change itself is documented even though the executed form is not:

| applied name | annotated source here |
|---|---|
| harden_plan_column_and_rpc_surface | 20260916_harden_plan_column_and_rpc_surface.sql |
| billing_amount_and_revenue_rpc | 20260916_billing_amount_and_revenue_rpc.sql |
| client_errors_sentinel | 20260916_client_errors_sentinel.sql |
| third_party_appended_attributes | 20260919_buy_and_append_third_party.sql |
| sharing_defaults_on_for_adults_opt_out_model | 20260919_sharing_default_on_opt_out.sql |
| apple_iap_and_derived_entitlement | 20260919_apple_iap_and_entitlement.sql |
| oauth_identity_claims_with_provenance | 20260920_oauth_identity_claims.sql |
| age_gate_and_data_sharing_consent | 20260918_data_sharing_programme.sql (group) |
| data_sharing_export_and_profile_fields | 20260918_data_sharing_programme.sql (group) |
| data_sharing_optout_rpc_and_first_policy | 20260918_data_sharing_programme.sql (group) |

The mapping for the three marked "(group)" is by subject rather than proven by checksum,
because one annotated file covers several applied statements. Treat it as a pointer, not
a guarantee.

Still unmirrored and with no annotated source:

    20260819193701  community_forum
    20260819202544  admin_v2_analytics_open_forum
    20260917130929  admin_item_diagnostics_rpc
    20260917133919  admin_item_diagnostics_hesitation
    20260918200037  birth_month_year_second_layer
    20260919135213  lock_down_sharing_functions_and_policy_table
    20260919165604  sharing_rpcs_for_opt_out_model

## Verifying, and finishing the job

The whole set can be checked against the database in one query:

    select version, name, md5(statements[1])
    from supabase_migrations.schema_migrations order by version;

and compared locally with, for a mirror:

    printf '%s' "$(cat <file>)" | md5sum

The trailing newline is excluded on purpose: the database stores the statement without
one and the file ends with one.

The supported way to complete this is `supabase db pull`, which needs the CLI and the
database password. It was not available where these were mirrored, so they were
transcribed through the MCP connector and checksum verified instead. If you run
`db pull`, expect it to produce the executed form for all 34 and to disagree with the
annotated files for the reason given at the top.

## Checksums as of 2026-09-21

    20260817194220  meridian_prep_core                            e34a1213ba3fb24447eab4a4635ae869  mirrored
    20260817213641  admin_bi                                      d271f1c5d9c4e0dcc00de3211bdfce1b  mirrored
    20260817214154  partner_crm                                   8c0d736d319b446a9191792d2e2b94fb  mirrored
    20260819193701  community_forum                               7a5ee191a0941c6fcd4b092f902f95ae
    20260819202544  admin_v2_analytics_open_forum                 7bd68ee4a9fd1a81c80202eea6f47658
    20260819202649  forum_screen_array_append_fix                 7078db6021af524f3d1aaa4e1bed7922  mirrored
    20260819205946  forum_last_author                             9c41b9bae6ee54baa09a26246f0a023f  mirrored
    20260916181333  harden_plan_column_and_rpc_surface            de899d0ab8ec8e41bc6fe2e519f21ba5
    20260916182036  billing_state_columns                         1fd59a2164bfcb38132c0734ad2cf5d6  mirrored
    20260916190622  revoke_public_execute_and_rls_initplan        c76a9d6190f99dc7740bb11bddb57393  mirrored
    20260916191004  billing_amount_and_revenue_rpc                c13b2058f075c8056edcab4af45877cb
    20260916191445  client_errors_sentinel                        1df2b7e18fbd3a3efb8c9204192d5bd5
    20260917130842  item_events_unlinkable_telemetry              0a9e8e80136b455091c49817b6f81b84  mirrored
    20260917130929  admin_item_diagnostics_rpc                    545b0527ff5be307cb5980a3f62be394
    20260917133719  item_events_interaction_detail                712caeb86b0578efd26c05634ba43f19  mirrored
    20260917133919  admin_item_diagnostics_hesitation             273449b3b39aee431069a634c359ddc0
    20260917145402  item_events_retention_400_days                2bbcba5c31936f53d8f05234c5a37ac4  mirrored
    20260917145439  item_events_retention_schedule                97bd5fa61e93fea1a8619d493c621745  mirrored
    20260917154849  social_posted_tracking                        68dc893df1e526695e5fd77996dbc54d  mirrored
    20260917182737  site_events_funnel_milestones                 463e579d74efeb3dfe53eb5adb7bee9d  mirrored
    20260917183609  admin_funnel_rpc                              67b58e72f532e63f789bab8681597b09  mirrored
    20260918194816  retention_site_events_and_client_errors       4c5d632158cca6bb8648d1db985217ec  mirrored
    20260918200002  age_gate_and_data_sharing_consent             2e692a02dbeca47603315e18e07526ce
    20260918200037  birth_month_year_second_layer                 6a0b6eebd9cdfab9e9225869411b6fc4
    20260918200209  data_sharing_export_and_profile_fields        35f6c31b1e601ec447e0dd14fe10b9ef
    20260918200854  data_sharing_optout_rpc_and_first_policy      dd2eff9cb114b0971f737078582b596b
    20260918203431  fix_profiles_trigger_firing_order             ae29ecdd69934f83b053b0b91baf57d3  mirrored
    20260918204223  sharing_eligibility_fires_on_every_update     2a88058a873cdc7b8a58cd7363d328a5  mirrored
    20260919132707  third_party_appended_attributes               bf0d412f2c9449a697a902d1dc7d0817
    20260919135213  lock_down_sharing_functions_and_policy_table  3be3f137856bdd5d6959c8415c92dfea
    20260919165509  sharing_defaults_on_for_adults_opt_out_model  1b2426b4be9a10e1d4bc7d20b9b21e4d
    20260919165604  sharing_rpcs_for_opt_out_model                691ee7ebb3781fd8f7047c29d6ad9d02
    20260919190937  apple_iap_and_derived_entitlement             a0bc855318e8b4af7954a62ae6e87b8f
    20260920145706  oauth_identity_claims_with_provenance         a1d711c5a3832e06d12a233ba0087bde

`PROPOSED_exam_states.sql` is not in that list because it was never applied. It is a
proposal.
