using Course.Data;
using Course.Data.Models;
using Microsoft.EntityFrameworkCore;

await using var db = new CourseDbContext();
await db.Database.EnsureCreatedAsync();

if (!await db.Projects.AnyAsync())
{
    db.Projects.AddRange(
        new Project { Name = "Каталог" },
        new Project { Name = "Трекер" });
    await db.SaveChangesAsync();
}

foreach (var project in await db.Projects.AsNoTracking().OrderBy(x => x.Name).ToListAsync())
    Console.WriteLine($"{project.Id}: {project.Name}");

