import { useEffect, useMemo, useState } from "react";

function ProjectCard({ project }) {
  return <article><h2>{project.name}</h2><p>{project.hours} ч. — {project.status}</p></article>;
}

export default function App() {
  const [projects, setProjects] = useState([]);
  const [query, setQuery] = useState("");
  const [state, setState] = useState("loading");

  useEffect(() => {
    const controller = new AbortController();
    fetch("/projects.json", { signal: controller.signal })
      .then(response => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); })
      .then(data => { setProjects(data); setState("ready"); })
      .catch(error => { if (error.name !== "AbortError") setState("error"); });
    return () => controller.abort();
  }, []);

  const visible = useMemo(() => {
    const value = query.trim().toLocaleLowerCase("ru-RU");
    return projects.filter(project => project.name.toLocaleLowerCase("ru-RU").includes(value));
  }, [projects, query]);

  return <main>
    <h1>Учебные проекты</h1>
    <label>Фильтр <input value={query} onChange={event => setQuery(event.target.value)} /></label>
    {state === "loading" && <p>Загрузка…</p>}
    {state === "error" && <p role="alert">Не удалось загрузить данные.</p>}
    {state === "ready" && visible.length === 0 && <p>Проекты не найдены.</p>}
    {state === "ready" && visible.map(project => <ProjectCard key={project.id} project={project} />)}
  </main>;
}

