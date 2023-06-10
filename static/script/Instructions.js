const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting){
            entry.target.classList.add('show_ins');
        }
        else{
            entry.target.classList.remove('show_ins');
        }
    });
});

const hiddenElements = document.querySelectorAll('.hidden_ins');
hiddenElements.forEach((el) => observer.observe(el));