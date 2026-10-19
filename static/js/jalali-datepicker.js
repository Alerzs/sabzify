(function () {
  const MONTHS = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'];
  const WEEKDAYS = ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'];
  const G_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  const J_DAYS = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29];
  const PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹';

  function toPersianDigits(value) {
    return String(value).replace(/\d/g, function (digit) {
      return PERSIAN_DIGITS[digit];
    });
  }

  function toEnglishDigits(value) {
    return String(value).replace(/[۰-۹٠-٩]/g, function (digit) {
      const persian = PERSIAN_DIGITS.indexOf(digit);
      if (persian >= 0) return String(persian);
      return String('٠١٢٣٤٥٦٧٨٩'.indexOf(digit));
    });
  }

  function isLeap(year) {
    return [1, 5, 9, 13, 17, 22, 26, 30].indexOf(year % 33) !== -1;
  }

  function monthLength(year, month) {
    if (month < 12) return J_DAYS[month - 1];
    return isLeap(year) ? 30 : 29;
  }

  function gregorianToJalali(gyear, gmonth, gday) {
    let gy = gyear - 1600;
    const gm = gmonth - 1;
    let dayNo = 365 * gy + Math.floor((gy + 3) / 4) - Math.floor((gy + 99) / 100) + Math.floor((gy + 399) / 400) + gday - 1 - 79;
    for (let i = 0; i < gm; i += 1) dayNo += G_DAYS[i];
    if (gm > 1 && ((gy % 4 === 0 && gy % 100 !== 0) || gy % 400 === 0)) dayNo += 1;

    const cycles = Math.floor(dayNo / 12053);
    dayNo %= 12053;
    let jy = 979 + 33 * cycles + 4 * Math.floor(dayNo / 1461);
    dayNo %= 1461;
    if (dayNo >= 366) {
      dayNo -= 1;
      jy += Math.floor(dayNo / 365);
      dayNo %= 365;
    }

    let index = 0;
    let finished = false;
    for (; index < 11; index += 1) {
      if (dayNo < J_DAYS[index]) {
        index -= 1;
        finished = true;
        break;
      }
      dayNo -= J_DAYS[index];
    }
    if (!finished) index = 10;
    return { year: jy, month: index + 2, day: dayNo + 1 };
  }

  function jalaliToGregorian(jyear, jmonth, jday) {
    let jy = jyear - 979;
    let dayNo = 365 * jy + Math.floor(jy / 33) * 8 + Math.floor((jy % 33 + 3) / 4) + jday - 1 + 79;
    for (let i = 0; i < jmonth - 1; i += 1) dayNo += J_DAYS[i];

    let gy = 1600 + 400 * Math.floor(dayNo / 146097);
    dayNo %= 146097;
    let leap = 1;
    if (dayNo >= 36525) {
      dayNo -= 1;
      gy += 100 * Math.floor(dayNo / 36524);
      dayNo %= 36524;
      if (dayNo >= 365) dayNo += 1;
      else leap = 0;
    }
    gy += 4 * Math.floor(dayNo / 1461);
    dayNo %= 1461;
    if (dayNo >= 366) {
      leap = 0;
      dayNo -= 1;
      gy += Math.floor(dayNo / 365);
      dayNo %= 365;
    }
    let index = 0;
    while (dayNo >= G_DAYS[index] + (index === 1 && leap)) {
      dayNo -= G_DAYS[index] + (index === 1 && leap);
      index += 1;
    }
    return { year: gy, month: index + 1, day: dayNo + 1 };
  }

  function compare(a, b) {
    return a.year - b.year || a.month - b.month || a.day - b.day;
  }

  function addMonths(date, count) {
    let month = date.month + count;
    let year = date.year;
    while (month > 12) {
      month -= 12;
      year += 1;
    }
    while (month < 1) {
      month += 12;
      year -= 1;
    }
    return { year: year, month: month, day: Math.min(date.day, monthLength(year, month)) };
  }

  function weekdayOf(date) {
    const gregorian = jalaliToGregorian(date.year, date.month, date.day);
    const jsDay = new Date(gregorian.year, gregorian.month - 1, gregorian.day).getDay();
    return (jsDay + 1) % 7;
  }

  function parseInput(value) {
    const text = toEnglishDigits(value).trim().replace(/[-.]/g, '/');
    const parts = text.split('/').map(function (part) { return part.trim(); }).filter(Boolean);
    if (parts.length !== 3) return null;
    let year = Number(parts[0]);
    const month = Number(parts[1]);
    let day = Number(parts[2]);
    if (year < 100 && day > 1300) {
      const swapped = year;
      year = day;
      day = swapped;
    }
    if (!year || month < 1 || month > 12 || day < 1 || day > monthLength(year, month)) return null;
    return { year: year, month: month, day: day };
  }

  function formatInput(date) {
    const month = String(date.month).padStart(2, '0');
    const day = String(date.day).padStart(2, '0');
    return toPersianDigits(date.year + '/' + month + '/' + day);
  }

  function todayJalali() {
    const now = new Date();
    return gregorianToJalali(now.getFullYear(), now.getMonth() + 1, now.getDate());
  }

  function setup(root) {
    const input = root.querySelector('input');
    const toggle = root.querySelector('.jalali-picker__toggle');
    const panel = root.querySelector('.jalali-picker__panel');
    if (!input || !toggle || !panel) return;

    input.readOnly = true;
    input.setAttribute('aria-haspopup', 'dialog');
    input.setAttribute('aria-controls', panel.id);
    toggle.setAttribute('aria-controls', panel.id);

    const today = todayJalali();
    const minDate = addMonths(today, -12);
    const maxDate = addMonths(today, 12);
    let view = parseInput(input.value) || today;
    let open = false;

    function canGoPrev() {
      return view.year > minDate.year || (view.year === minDate.year && view.month > minDate.month);
    }

    function canGoNext() {
      return view.year < maxDate.year || (view.year === maxDate.year && view.month < maxDate.month);
    }

    function render() {
      const selected = parseInput(input.value);
      const days = monthLength(view.year, view.month);
      const offset = weekdayOf({ year: view.year, month: view.month, day: 1 });
      const cells = [];
      for (let i = 0; i < offset; i += 1) cells.push('<span></span>');
      for (let day = 1; day <= days; day += 1) {
        const date = { year: view.year, month: view.month, day: day };
        const disabled = compare(date, today) < 0 || compare(date, maxDate) > 0;
        const classes = ['jalali-picker__day'];
        if (selected && compare(date, selected) === 0) classes.push('is-selected');
        if (compare(date, today) === 0) classes.push('is-today');
        const label = toPersianDigits(day) + ' ' + MONTHS[view.month - 1] + ' ' + toPersianDigits(view.year);
        cells.push(
          '<button type="button" class="' + classes.join(' ') + '" data-day="' + day + '"' +
          (disabled ? ' disabled' : '') +
          ' aria-label="' + label + '">' + toPersianDigits(day) + '</button>'
        );
      }

      panel.innerHTML =
        '<div class="jalali-picker__header">' +
          '<button type="button" class="jalali-picker__nav" data-nav="-1"' + (canGoPrev() ? '' : ' disabled') + ' aria-label="ماه قبل">›</button>' +
          '<div class="jalali-picker__title">' + MONTHS[view.month - 1] + ' ' + toPersianDigits(view.year) + '</div>' +
          '<button type="button" class="jalali-picker__nav" data-nav="1"' + (canGoNext() ? '' : ' disabled') + ' aria-label="ماه بعد">‹</button>' +
        '</div>' +
        '<div class="jalali-picker__weekdays">' + WEEKDAYS.map(function (name) {
          return '<span>' + name + '</span>';
        }).join('') + '</div>' +
        '<div class="jalali-picker__days">' + cells.join('') + '</div>' +
        '<div class="jalali-picker__footer">' +
          '<button type="button" data-action="today">امروز</button>' +
          '<button type="button" data-action="clear">پاک کردن</button>' +
        '</div>';
    }

    function place() {
      panel.classList.remove('is-above');
      const rect = panel.getBoundingClientRect();
      const spaceBelow = window.innerHeight - rect.bottom;
      if (spaceBelow < 12 && root.getBoundingClientRect().top > rect.height + 12) {
        panel.classList.add('is-above');
      }
    }

    function show() {
      if (open) return;
      const selected = parseInput(input.value);
      view = selected ? { year: selected.year, month: selected.month, day: 1 } : { year: today.year, month: today.month, day: 1 };
      render();
      panel.hidden = false;
      open = true;
      toggle.setAttribute('aria-expanded', 'true');
      place();
    }

    function hide() {
      panel.hidden = true;
      open = false;
      toggle.setAttribute('aria-expanded', 'false');
    }

    function choose(date) {
      input.value = formatInput(date);
      input.dispatchEvent(new Event('change', { bubbles: true }));
      hide();
    }

    input.addEventListener('click', show);
    input.addEventListener('focus', show);
    toggle.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      if (open) hide();
      else show();
    });

    panel.addEventListener('mousedown', function (event) {
      event.preventDefault();
    });

    panel.addEventListener('click', function (event) {
      event.stopPropagation();
      const nav = event.target.closest('[data-nav]');
      if (nav && !nav.disabled) {
        const direction = Number(nav.dataset.nav);
        const next = addMonths({ year: view.year, month: view.month, day: 1 }, direction);
        view = { year: next.year, month: next.month, day: 1 };
        render();
        place();
        const fresh = panel.querySelector('[data-nav="' + direction + '"]');
        if (fresh && !fresh.disabled) fresh.focus();
        return;
      }
      const day = event.target.closest('[data-day]');
      if (day && !day.disabled) {
        choose({ year: view.year, month: view.month, day: Number(day.dataset.day) });
        return;
      }
      const action = event.target.closest('[data-action]');
      if (!action) return;
      if (action.dataset.action === 'today') choose(today);
      if (action.dataset.action === 'clear') {
        input.value = '';
        input.dispatchEvent(new Event('change', { bubbles: true }));
        hide();
      }
    });

    document.addEventListener('click', function (event) {
      if (!open) return;
      const path = typeof event.composedPath === 'function' ? event.composedPath() : [];
      if (path.indexOf(root) !== -1 || root.contains(event.target)) return;
      hide();
    });
    document.addEventListener('keydown', function (event) {
      if (open && event.key === 'Escape') hide();
    });
  }

  if (typeof document !== 'undefined') {
    document.querySelectorAll('[data-jalali-picker]').forEach(setup);
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { gregorianToJalali: gregorianToJalali, jalaliToGregorian: jalaliToGregorian, isLeap: isLeap };
  }
})();
