/*
1. fetch("/api/departures")
2. convert response to JSON
3. for each departure:
     - create HTML
4. insert into #departures
*/


async function getData() {
    //TODO: this is bad should be in a config
    const url = "/api/departures";
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const result = await response.json();
        return result
    } catch (error) {
        console.error(error.message);
    }
}




// 1. fetch departures
//2. convert data 

//3. for each departure:
//     - create HTML
async function main() {
    const departures = await getData();

    const container = document.getElementById("departures");

    container.innerHTML = "";

    for (let i = 0; i < departures.length; i++) {
        let obj = departures[i];

        container.innerHTML += `
            <div>
                <span>${obj.line}</span>
                <span>${obj.destination}</span>
                <span>${obj.minutes_to_departure} min</span>
            </div>
        `;
    }
}

main();