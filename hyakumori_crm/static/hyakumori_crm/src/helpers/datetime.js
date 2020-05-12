import { formatDistanceToNow, parseISO, format, toDate } from "date-fns";
import { zonedTimeToUtc } from "date-fns-tz";

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

export function commonDatetimeFormat(datetime) {
  return datetime && format(new Date(datetime), "yyyy-MM-dd HH:mm");
}

export function toUtcDatetime(datetime, toISOString = true) {
  const currentTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const utcDateTime = zonedTimeToUtc(datetime, currentTimezone);
  if (toISOString) {
    return utcDateTime.toISOString();
  } else {
    return utcDateTime;
  }
}

/**
 * Example 1: 2020-05-20 and stripTime = false
 * -> 2020-05-20 12:00:00 (by defaultIfEmpty)
 *
 * Example 2: 2020-05-20 and stripTime = true
 * -> 2020-05-20
 *
 * @param datetime
 * @param defaultIfEmpty
 * @returns {string}
 */
export function dateTimeKeywordSearchFormat(
  datetime,
  defaultIfEmpty = undefined,
) {
  if (!defaultIfEmpty) {
    defaultIfEmpty = {
      year: 2020,
      month: 12,
      day: 1,
      hours: 12,
      minutes: 0,
      seconds: 0,
    };
  }
  const date = toUtcDatetime(datetime, false);
  // const date = new Date(utcDateTime);
  const parts = {
    year: date.getFullYear(),
    month: date.getMonth(),
    day: date.getDate(),
    hours: date.getHours(),
    minutes: date.getMinutes(),
    seconds: date.getSeconds(),
  };
  for (let key of Object.keys(parts)) {
    if (parts[key] === 0 && key in defaultIfEmpty) {
      parts[key] = defaultIfEmpty[key];
    }
  }

  //2020
  //2020-01
  //2020-01-30
  //2020-01-30 12:00
  //2020-01-30 13:30
  if (parts.month === 0) {
    return parts.year;
  }
  if (parts.month > 0 && parts.day === 0) {
    return `${parts.year}-${parts.month}`;
  }

  if (parts.day > 0) {
    if (parts.hours === 0) {
      return `${parts.year}-${parts.month}-${parts.day}`;
    }

    let date = new Date(
      parts.year,
      parts.month,
      parts.day,
      parts.hours,
      parts.minutes,
      parts.seconds,
    );
  }

  return isoDate;
}

export function getTime(datetime) {
  return format(new Date(datetime), "HH:mm");
}

export function getDate(datetime) {
  return format(new Date(datetime), "yyyy-MM-dd");
}
