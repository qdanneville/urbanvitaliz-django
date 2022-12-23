import Alpine from 'alpinejs'

function ProjectNavigation() {
    return {
        init() {
            const navigationEl = this.$refs.navigation
            const headerElHeight = document.getElementsByClassName('navbar')[0].offsetHeight;

            console.log('project nav ready')
            console.log('nav el : ', navigationEl);
            console.log('header el : ', headerElHeight);

            let lastKnownScrollPosition = 0;
            let ticking = false;

            function doSomething(scrollPos) {
                // Do something with the scroll position
                console.log('scroll pos : ', scrollPos);
                console.log(navigationEl.offsetTop - headerElHeight - 10);

                if (scrollPos >= navigationEl.offsetTop - headerElHeight - 10) {
                    console.log('nav is sticky !!')
                    navigationEl.classList.add('is-sticky')
                } else navigationEl.classList.remove('is-sticky')
            }

            document.addEventListener("scroll", (event) => {
                lastKnownScrollPosition = window.scrollY;

                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        doSomething(lastKnownScrollPosition);
                        ticking = false;
                    });

                    ticking = true;
                }
            });

        }
    }
}

Alpine.data("ProjectNavigation", ProjectNavigation)
