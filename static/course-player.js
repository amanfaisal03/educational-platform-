(() => {
    'use strict';
    const lessons = [...document.querySelectorAll('.lesson-item')];
    const video = document.getElementById('lesson-video');
    const pdf = document.getElementById('lesson-pdf');
    const play = document.getElementById('play-button');
    const message = document.getElementById('player-message');
    const previous = document.getElementById('previous-lesson');
    const complete = document.getElementById('complete-lesson');
    const showVideo = document.getElementById('show-video');
    const showPdf = document.getElementById('show-pdf');
    const openPdf = document.getElementById('open-pdf');
    const completed = new Set();
    let selected = -1;
    let mode = '';

    function displayMaterial(type) {
        const lesson = lessons[selected].dataset;
        mode = type;
        video.pause();
        video.hidden = type !== 'video';
        pdf.hidden = type !== 'pdf';
        play.hidden = type !== 'video';
        message.hidden = Boolean(type);
        showVideo.setAttribute('aria-pressed', String(type === 'video'));
        showPdf.setAttribute('aria-pressed', String(type === 'pdf'));
        pdf.removeAttribute('src');
        if (type === 'video') {
            video.src = lesson.video;
            video.load();
        } else {
            video.removeAttribute('src');
            video.load();
            if (type === 'pdf') pdf.src = lesson.pdf;
            else message.textContent = 'لم تُضف مواد لهذا الدرس بعد.';
        }
    }

    function selectLesson(index) {
        if (index < 0 || index >= lessons.length) return;
        selected = index;
        const lesson = lessons[index].dataset;
        lessons.forEach((item, position) => item.setAttribute('aria-pressed', String(position === index)));
        document.getElementById('lesson-title').textContent = lesson.title;
        document.getElementById('unit-title').textContent = lesson.unitTitle;
        previous.disabled = index === 0;
        complete.disabled = !lesson.video && !lesson.pdf;
        complete.textContent = index === lessons.length - 1 ? 'إنهاء الدرس' : 'إنهاء الدرس والتالي';
        showVideo.hidden = !lesson.video;
        showPdf.hidden = !lesson.pdf;
        openPdf.hidden = !lesson.pdf;
        if (lesson.pdf) openPdf.href = lesson.pdf;
        else openPdf.removeAttribute('href');
        displayMaterial(lesson.video ? 'video' : (lesson.pdf ? 'pdf' : ''));
    }

    lessons.forEach((lesson, index) => lesson.addEventListener('click', () => selectLesson(index)));
    showVideo.addEventListener('click', () => displayMaterial('video'));
    showPdf.addEventListener('click', () => displayMaterial('pdf'));
    play.addEventListener('click', () => {
        video.play().catch(() => {
            message.textContent = 'تعذّر تشغيل الفيديو. حاول تشغيله من عناصر التحكم أو اختر الدرس مجدداً.';
            message.hidden = false;
            play.hidden = true;
        });
    });
    video.addEventListener('play', () => { play.hidden = true; message.hidden = true; });
    video.addEventListener('error', () => {
        if (mode !== 'video' || !video.getAttribute('src')) return;
        play.hidden = true;
        message.textContent = 'تعذّر تحميل الفيديو. تحقق من اتصالك ومن اشتراكك في الدورة ثم حاول مجدداً.';
        message.hidden = false;
    });
    previous.addEventListener('click', () => selectLesson(selected - 1));
    complete.addEventListener('click', () => {
        if (selected < 0) return;
        completed.add(lessons[selected].dataset.lessonId);
        lessons[selected].querySelector('.lesson-complete').hidden = false;
        const percent = Math.round(completed.size / lessons.length * 100);
        document.getElementById('course-progress').value = percent;
        document.getElementById('progress-label').textContent = `${percent}% مكتمل`;
        if (selected < lessons.length - 1) selectLesson(selected + 1);
        else { complete.textContent = 'تم إنهاء الدرس ✓'; complete.disabled = true; }
    });
    if (lessons.length) {
        const initialUnit = document.querySelector('.course-layout').dataset.initialUnit;
        const initialIndex = lessons.findIndex(lesson => lesson.dataset.unitId === initialUnit);
        selectLesson(initialIndex >= 0 ? initialIndex : 0);
    }
})();
