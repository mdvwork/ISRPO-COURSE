namespace Course.Data.Models;

public sealed class Project
{
    public int Id { get; set; }
    public required string Name { get; set; }
    public ICollection<TaskItem> Tasks { get; set; } = [];
}

