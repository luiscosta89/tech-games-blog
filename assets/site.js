document.querySelectorAll('[data-video]').forEach((button) => {
  button.addEventListener('click', () => {
    const id = button.dataset.video;
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1`;
    iframe.title = button.getAttribute('aria-label') || 'Vídeo do YouTube';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    button.parentElement.replaceChildren(iframe);
  });
});

const headings = [...document.querySelectorAll('.prose h2')];
const tocLinks = [...document.querySelectorAll('.toc a')];
if (headings.length && 'IntersectionObserver' in window) {
  const byId = new Map(tocLinks.map((link) => [link.hash.slice(1), link]));
  const observer = new IntersectionObserver((entries) => {
    entries.filter((entry) => entry.isIntersecting).forEach((entry) => {
      tocLinks.forEach((link) => link.classList.remove('active'));
      byId.get(entry.target.id)?.classList.add('active');
    });
  }, { rootMargin: '-18% 0px -72% 0px' });
  headings.forEach((heading) => observer.observe(heading));
}
