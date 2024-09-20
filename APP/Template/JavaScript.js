const readline = require('readline');

function add(a, b) {
    return a + b;
}

function main() {
    console.log("Welcome to the JavaScript Template!");

    // Example of using a function
    let result = add(5, 3);
    console.log(`5 + 3 = ${result}`);

    // Array methods example
    let numbers = [1, 2, 3, 4, 5];
    let squares = numbers.map(x => x * x);
    console.log(`Squares from 1 to 5: ${squares}`);

    // Error handling example
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.question("Enter a number to divide 10: ", (answer) => {
        try {
            let value = Number(answer);
            if (isNaN(value)) throw new Error("Not a valid number");
            console.log(`10 / ${value} = ${10 / value}`);
        } catch (error) {
            console.error(error.message);
        } finally {
            rl.close();
            console.log("Press any key to exit...");
            process.stdin.resume(); // Keep the process open
            process.stdin.on('data', () => {
                process.exit(); // Exit when a key is pressed
            });
        }
    });
}

main();
