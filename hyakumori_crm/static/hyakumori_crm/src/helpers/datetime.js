import { formatDistanceToNow, parseISO, format } from "date-fns";

import { ja } from "date-fns/locale";

export function fromNow(dateTimeString) {
  if (!dateTimeString) {
    return;
  }
  return formatDistanceToNow(parseISO(dateTimeString), {
    addSuffix: true,
    locale: ja,
  });
}

export function archiveDatetimeFormat(datetime) {
  return format(new Date(datetime), "yyyy/MM/dd HH:mm");
}
