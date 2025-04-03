// 메인 배너 슬라이드 효과
const bannerSlider = document.querySelector('.banner-slider');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
let currentIndex = 0;
const bannerItems = bannerSlider.children;
const bannerCount = bannerItems.length;

function showBanner(index) {
  for (let i = 0; i < bannerCount; i++) {
    bannerItems[i].style.display = 'none';
  }
  bannerItems[index].style.display = 'block';
}

prevBtn.addEventListener('click', () => {
  currentIndex = (currentIndex - 1 + bannerCount) % bannerCount;
  showBanner(currentIndex);
});

nextBtn.addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % bannerCount;
  showBanner(currentIndex);
});

showBanner(currentIndex);

// 스크롤 애니메이션
const animatedElements = document.querySelectorAll('.animate');

function animateOnScroll() {
  animatedElements.forEach(element => {
    const elementTop = element.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if (elementTop < windowHeight * 0.8) {
      element.classList.add('fade-in');
    } else {
      element.classList.remove('fade-in');
    }
  });
}

window.addEventListener('scroll', animateOnScroll);