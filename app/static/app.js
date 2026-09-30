/* --- Fetch data --- */

async function getData() {
  //TODO: this is bad should be in a config
  const url = "/api/departures";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error.message);
  }
}

async function main() {
  const departures = await getData();

  const container = document.getElementById("departures");

  buildBoard(departures);
}

/* --- Displaying data --- */

const headerRubrics = ["Line", "To", "Time"];

const COLUMN_WIDTHS = {
  line: 4,
  destination: 18,
  minutes: 16,
};

function buildBoard(departures_data) {
  // main do stuff

  const board = document.getElementById("departure-board");

  // auto-size
  COLUMN_WIDTHS.line = Math.max(
    headerRubrics[0].length,
    ...departures_data.map((d) => String(d.line).length),
  );

  COLUMN_WIDTHS.destination = Math.max(
    headerRubrics[1].length,
    ...departures_data.map((d) => d.destination.length),
  );

  COLUMN_WIDTHS.minutes = Math.max(
    headerRubrics[2].length,
    ...departures_data.map((d) => d.display_time.length),
  );

  COLUMN_WIDTHS.day = Math.max(
    0,
    ...departures_data.map((d) => (d.day_label ?? "").length),
  );

  //Build header row | Line NR | Line name | time |

  topRow = buildRow(headerRubrics[0], headerRubrics[1], headerRubrics[2]);

  board.appendChild(topRow);
  // loop through the data list of dict objects

  for (let i = 0; i < departures_data.length; i++) {
    let data_dict = departures_data[i];

    newRow = buildRow(
      data_dict.line,
      data_dict.destination,
      data_dict.display_time,
      data_dict.day_label,
    );
    board.appendChild(newRow);
  }

  //victory dance
}

function buildRow(lineNr, lineName, minToDeparture, dayLabel = "") {
  const row = document.createElement("div");
  row.className = "row";

  // Format all data
  const formattedLine = formatField(lineNr, COLUMN_WIDTHS.line);
  const formattedDestination = formatField(lineName, COLUMN_WIDTHS.destination);
  const formattedMinutes = formatField(minToDeparture, COLUMN_WIDTHS.minutes);

  //split each word into retro word

  //FIXME: All these for loops could be helper functions to avoid code duplication
  for (let i = 0; i < formattedLine.length; i++) {
    const character = formattedLine[i];
    const span = document.createElement("span");
    span.className = `letter letter-${character}`;
    row.appendChild(span);
  }

  row.appendChild(createSpace());

  for (let i = 0; i < formattedDestination.length; i++) {
    const character = formattedDestination[i];
    const span = document.createElement("span");
    span.className = `letter letter-${character}`;
    row.appendChild(span);
  }

  row.appendChild(createSpace());

  for (let i = 0; i < formattedMinutes.length; i++) {
    const character = formattedMinutes[i];
    const span = document.createElement("span");
    span.className = `letter letter-${character}`;
    row.appendChild(span);
  }

  // render the day label

  if (COLUMN_WIDTHS.day > 0) {
    row.appendChild(createSpace());
  }

  const formattedDay = formatField(dayLabel, COLUMN_WIDTHS.day);

  for (const character of formattedDay) {
    const span = document.createElement("span");
    span.className =
      character === " " ? "letter letter-blank" : `letter letter-${character}`;
    row.appendChild(span);
  }

  return row;
}

function formatField(value, width) {
  const text = String(value).toUpperCase();

  if (text.length > width) {
    return text.slice(0, width);
  }

  return text.padEnd(width, " ");
}

function createSpace() {
  const span = document.createElement("span");
  span.className = "letter letter-blank";
  return span;
}

document.addEventListener("DOMContentLoaded", () => {
  main();
});
