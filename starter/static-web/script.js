const form = document.querySelector("#filter-form");
const query = document.querySelector("#query");
const list = document.querySelector("#projects");
const status = document.querySelector("#status");
let projects = [];

function filtered(items, value) {
  const normalized = value.trim().toLocaleLowerCase("ru-RU");
  return items.filter(item => item.name.toLocaleLowerCase("ru-RU").includes(normalized));
}

function render(items) {
  list.replaceChildren();
  for (const project of items) {
    const card = document.createElement("article");
    card.className = "project-card";
    const heading = document.createElement("h2");
    heading.textContent = project.name;
    const details = document.createElement("p");
    details.textContent = `${project.hours} ч. — ${project.status}`;
    card.append(heading, details);
    list.append(card);
  }
  status.textContent = items.length ? `Найдено: ${items.length}` : "Проекты не найдены";
}

form.addEventListener("submit", event => {
  event.preventDefault();
  render(filtered(projects, query.value));
});

try {
  const response = await fetch("data/projects.json");
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  projects = await response.json();
  render(projects);
} catch (error) {
  status.textContent = "Не удалось загрузить проекты";
  console.error(error);
}

