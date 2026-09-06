/* Renewal Health v2 interactions */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.querySelector('.v2-header');
  var hero = document.querySelector('.home-hero, .page-hero');

  // sticky header: turn from transparent-over-hero to solid frosted after the hero
  if(header){
    var solidAt = 10;
    function measure(){
      solidAt = hero ? Math.max(10, hero.offsetHeight - 64) : 10;
    }
    measure();
    window.addEventListener('resize', measure, {passive:true});
    function onScroll(){ header.classList.toggle('scrolled', window.scrollY > solidAt); }
    window.addEventListener('scroll', onScroll, {passive:true});
    onScroll();
  }

  // mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.v2-nav');
  if(toggle && nav){
    toggle.addEventListener('click', function(){ nav.classList.toggle('open'); });
    nav.querySelectorAll('.has-drop>a').forEach(function(a){
      a.addEventListener('click', function(e){
        if(window.innerWidth <= 960){ e.preventDefault(); a.parentElement.classList.toggle('open'); }
      });
    });
  }

  // reveal: ONLY the first content section animates in, once, on load.
  // Everything below is already in place (no scroll reveal).
  var intro = document.querySelector('.intro-reveal');
  if(intro){
    if(reduce){
      intro.classList.add('in');
    }else{
      requestAnimationFrame(function(){ requestAnimationFrame(function(){ intro.classList.add('in'); }); });
    }
  }

  // home hero: one-time entrance.
  // A solid blue-violet curtain covers the viewport; a large naturalistic
  // dragonfly flies the diagonal from the bottom-left corner to the top-right
  // corner and the curtain is wiped away along that diagonal. When the flight
  // ends BOTH nodes are removed from the DOM, so nothing can linger over the
  // page or follow the reader while scrolling.
  var homeHero = document.querySelector('.home-hero');
  if(homeHero){ homeHero.classList.add('opened'); }

  var curtains = [].slice.call(document.querySelectorAll('.hero-curtain'));
  var flier = document.querySelector('.df-reveal');
  if(curtains.length || flier){
    // QA hook: ?stage=flight freezes the entrance mid-flight (nothing removed)
    var frozen = /(^|[?&])stage=flight(&|$)/.test(location.search);
    if(frozen){
      document.documentElement.classList.add('df-freeze');
      // optional &t=<seconds> seeks the frozen frame (default is 0.75s in CSS)
      var seek = /(^|[?&])t=([0-9.]+)/.exec(location.search);
      if(seek){
        curtains.concat([flier]).forEach(function(el){
          if(el){ el.style.animationDelay = '-' + seek[2] + 's'; }
        });
      }
    }else if(reduce){
      // reduced motion: no curtain, no flight, finished hero immediately
      removeEntrance();
    }else{
      var done = false;
      function finish(){
        if(done){ return; }
        done = true;
        removeEntrance();
      }
      if(flier){ flier.addEventListener('animationend', function(e){
        if(e.animationName === 'df-cross'){ finish(); }
      }); }
      if(curtains.length && !flier){ curtains[0].addEventListener('animationend', function(e){
        if(e.animationName === 'part-top' || e.animationName === 'part-bot'){ finish(); }
      }); }
      // hard fallback: the entrance is 0.05s delay + 4s flight = 4.05s
      setTimeout(finish, 4400);
    }
  }
  function removeEntrance(){
    curtains.concat([flier]).forEach(function(el){
      if(el && el.parentNode){ el.parentNode.removeChild(el); }
    });
    curtains = []; flier = null;
    document.documentElement.setAttribute('data-entrance', 'done');
  }

  // gentle hero parallax
  var heroImg = document.querySelector('[data-parallax]');
  if(heroImg && !reduce){
    window.addEventListener('scroll', function(){
      var y = window.scrollY;
      if(y < 900){ heroImg.style.transform = 'translateY(' + (y*0.12) + 'px) scale(1.04)'; }
    }, {passive:true});
  }

  // ---- book promo card (bottom right) --------------------------------------
  // Lynette's book: Nothing Missing, Nothing Broken. No expiry (a book does not
  // pass like an event). Dismissal is remembered per visitor. Swap the CTA href
  // for the purchase link (Amazon etc.) once Lynette has one.
  (function(){
    var EVENT = {
      key: 'rh-promo-book-nmnb',
      url: 'book.html'
    };
    var preview = /(^|[?&])promo=now(&|$)/.test(location.search);
    try { if(!preview && localStorage.getItem(EVENT.key) === 'dismissed') return; } catch(e){}

    var card = document.createElement('aside');
    card.className = 'promo-card';
    card.setAttribute('role', 'complementary');
    card.setAttribute('aria-label', 'Announcement: Nothing Missing, Nothing Broken, the new book by Lynette Wing');
    card.innerHTML =
      '<button class="promo-close" type="button" aria-label="Close book notice">&times;</button>' +
      '<p class="promo-kicker">New from Lynette</p>' +
      '<h2 class="promo-title">Nothing Missing, Nothing Broken</h2>' +
      '<p class="promo-talk">The new book by <em>Lynette Wing RN, HHP</em></p>' +
      '<p class="promo-note">A look at whole-person healing: why your body is not broken, and how renewal begins at the root.</p>' +
      '<a class="promo-cta" href="' + EVENT.url + '">Ask Lynette about the book</a>';

    function dismiss(){
      card.classList.remove('is-open');
      try { localStorage.setItem(EVENT.key, 'dismissed'); } catch(e){}
      setTimeout(function(){ if(card.parentNode){ card.parentNode.removeChild(card); } }, 350);
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e){ if(e.key === 'Escape' || e.keyCode === 27){ dismiss(); } }

    card.querySelector('.promo-close').addEventListener('click', dismiss);
    document.addEventListener('keydown', onKey);

    function show(){
      if(document.body.contains(card)) return;
      document.body.appendChild(card);
      requestAnimationFrame(function(){
        requestAnimationFrame(function(){ card.classList.add('is-open'); });
      });
    }
    // hold it back until the hero entrance is done and the reader has settled.
    // ?promo=now shows it immediately (preview/QA hook, also bypasses dismissal).
    if(/(^|[?&])promo=now(&|$)/.test(location.search)){ show(); return; }
    var delay = document.querySelector('.home-hero') ? 5200 : 2200;
    setTimeout(show, reduce ? 800 : delay);
  })();

})();
