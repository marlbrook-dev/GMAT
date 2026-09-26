create or replace function forum_screen(txt text) returns jsonb
language plpgsql immutable as $$
declare
  t text := lower(coalesce(txt, ''));
  reasons text[] := '{}';
  hide boolean := false;
  letters int;
  caps_ratio numeric;
begin
  if (char_length(t) - char_length(replace(t, 'http', ''))) / 4 > 2 then
    reasons := array_append(reasons, 'many_links');
  end if;
  if t ~ '(saw this on (my|the) (real |actual )?(gmat|gre|lsat|mcat|exam)|on my actual (gmat|gre|lsat|mcat|exam)|memorized (this |it )?from the (test|exam)|real exam question|actual exam question|question from my (gmat|gre|lsat|mcat) (today|yesterday))' then
    reasons := array_append(reasons, 'possible_real_exam_content'); hide := true;
  end if;
  if t ~ '(guaranteed score|score guarantee|pay someone to take|take (the|your) (exam|test) for you|proxy test taker|buy (an? )?(essay|answers))' then
    reasons := array_append(reasons, 'cheating_service'); hide := true;
  end if;
  if t ~ '\y(fuck|shit|bitch|asshole|cunt|nigger|faggot)\y' then
    reasons := array_append(reasons, 'abusive_language');
    if t ~ '\y(nigger|faggot|cunt)\y' then hide := true; end if;
  end if;
  if t ~ '(whatsapp|telegram)[^a-z]{0,6}(me|us|group)|\+\d{10,}' then
    reasons := array_append(reasons, 'contact_solicitation');
  end if;
  letters := char_length(regexp_replace(coalesce(txt, ''), '[^A-Za-z]', '', 'g'));
  if letters > 60 then
    caps_ratio := char_length(regexp_replace(coalesce(txt, ''), '[^A-Z]', '', 'g'))::numeric / letters;
    if caps_ratio > 0.7 then reasons := array_append(reasons, 'shouting'); end if;
  end if;
  return jsonb_build_object('flagged', cardinality(reasons) > 0,
    'reason', array_to_string(reasons, ','), 'hide', hide);
end $$;
