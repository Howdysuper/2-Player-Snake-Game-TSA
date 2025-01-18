const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const CELL_SIZE = 20;
const WIDTH = canvas.width;
const HEIGHT = canvas.height;
const TARGET_SCORE = 10;

const COLORS = {
    player1: 'blue',
    player2: 'green',
    apple: 'red',
    background: 'black'
};

const DIRECTIONS = {
    UP: { x: 0, y: -1 },
    DOWN: { x: 0, y: 1 },
    LEFT: { x: -1, y: 0 },
    RIGHT: { x: 1, y: 0 }
};

class Snake {
    constructor(color, startX, startY) {
        this.color = color;
        this.body = [{ x: startX, y: startY }];
        this.direction = this.getRandomDirection();
        this.score = 0;
        this.growNextMove = false;
    }

    getRandomDirection() {
        const directions = [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.LEFT, DIRECTIONS.RIGHT];
        return directions[Math.floor(Math.random() * directions.length)];
    }

    move() {
        const head = this.body[0];
        const newHead = { x: head.x + this.direction.x, y: head.y + this.direction.y };

        if (this.growNextMove) {
            this.body.unshift(newHead);
            this.growNextMove = false;
        } else {
            this.body.pop();
            this.body.unshift(newHead);
        }
    }

    grow() {
        this.growNextMove = true;
    }

    changeDirection(newDirection) {
        // Prevent 180-degree turn
        if (this.direction.x + newDirection.x !== 0 || this.direction.y + newDirection.y !== 0) {
            this.direction = newDirection;
        }
    }

    draw() {
        for (const segment of this.body) {
            ctx.fillStyle = this.color;
            ctx.fillRect(segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
    }
}

function getRandomApplePosition(snake1, snake2) {
    let position;
    while (true) {
        position = {
            x: Math.floor(Math.random() * (WIDTH / CELL_SIZE)),
            y: Math.floor(Math.random() * (HEIGHT / CELL_SIZE))
        };
        if (!snake1.body.some(segment => segment.x === position.x && segment.y === position.y) &&
            !snake2.body.some(segment => segment.x === position.x && segment.y === position.y)) {
            break;
        }
    }
    return position;
}

const snake1 = new Snake(COLORS.player1, WIDTH / (4 * CELL_SIZE), HEIGHT / (2 * CELL_SIZE));
const snake2 = new Snake(COLORS.player2, (3 * WIDTH) / (4 * CELL_SIZE), HEIGHT / (2 * CELL_SIZE));
let apple = getRandomApplePosition(snake1, snake2);

function gameLoop() {
    update();
    draw();
    checkGameOver();
    if (snake1.score >= TARGET_SCORE || snake2.score >= TARGET_SCORE) {
        alert(`${snake1.score >= TARGET_SCORE ? 'Player 1' : 'Player 2'} wins!`);
        resetGame();
    } else {
        requestAnimationFrame(gameLoop);
    }
}

function update() {
    snake1.move();
    snake2.move();
    checkAppleCollision(snake1);
    checkAppleCollision(snake2);
}

function draw() {
    ctx.fillStyle = COLORS.background;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    snake1.draw();
    snake2.draw();
    ctx.fillStyle = COLORS.apple;
    ctx.fillRect(apple.x * CELL_SIZE, apple.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
}

function checkAppleCollision(snake) {
    const head = snake.body[0];
    if (head.x === apple.x && head.y === apple.y) {
        snake.grow();
        snake.score++;
        apple = getRandomApplePosition(snake1, snake2);
    }
}

function checkGameOver() {
    checkCollision(snake1);
    checkCollision(snake2);
}

function checkCollision(snake) {
    const head = snake.body[0];
    if (head.x < 0 || head.x >= WIDTH / CELL_SIZE || head.y < 0 || head.y >= HEIGHT / CELL_SIZE ||
        snake.body.slice(1).some(segment => segment.x === head.x && segment.y === head.y)) {
        alert(`${snake.color === COLORS.player1 ? 'Player 1' : 'Player 2'} crashes! Game over.`);
        resetGame();
    }
}

function resetGame() {
    snake1.body = [{ x: WIDTH / (4 * CELL_SIZE), y: HEIGHT / (2 * CELL_SIZE) }];
    snake1.score = 0;
    snake1.direction = snake1.getRandomDirection();

    snake2.body = [{ x: (3 * WIDTH) / (4 * CELL_SIZE), y: HEIGHT / (2 * CELL_SIZE) }];
    snake2.score = 0;
    snake2.direction = snake2.getRandomDirection();

    apple = getRandomApplePosition(snake1, snake2);
    requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'w': snake1.changeDirection(DIRECTIONS.UP); break;
        case 's': snake1.changeDirection(DIRECTIONS.DOWN); break;
        case 'a': snake1.changeDirection(DIRECTIONS.LEFT); break;
        case 'd': snake1.changeDirection(DIRECTIONS.RIGHT); break;
        case 'ArrowUp': snake2.changeDirection(DIRECTIONS.UP); break;
        case 'ArrowDown': snake2.changeDirection(DIRECTIONS.DOWN); break;
        case 'ArrowLeft': snake2.changeDirection(DIRECTIONS.LEFT); break;
        case 'ArrowRight': snake2.changeDirection(DIRECTIONS.RIGHT); break;
    }
});

requestAnimationFrame(gameLoop);
