namespace Course.Data.Models;

public sealed class TaskItem
{
    public int Id { get; set; }
    public required string Title { get; set; }
    public bool IsDone { get; set; }
    public int ProjectId { get; set; }
    public Project? Project { get; set; }
}

