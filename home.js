window.onload = () => {
const scroll = document.querySelector('.ScrollMovies'); //contains all the movies that need scrolling
const leftArrow = document.querySelector('.LeftArrow');
const rightArrow = document.querySelector('.RightArrow');

const scrollAmount = 400; //how far it wil scroll

rightArrow.addEventListener('click', () => {
    scroll.scrollBy({ left: scrollAmount, behavior: 'smooth' }); //when you click the right arrow it will scroll 400 pixels forward
});

leftArrow.addEventListener('click', () => {
    scroll.scrollBy({ left: -scrollAmount, behavior: 'smooth' }); //when left arrow is clicked imgs will be movies 400 pixels backwards
});
}