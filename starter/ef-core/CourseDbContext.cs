using Course.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace Course.Data;

public sealed class CourseDbContext : DbContext
{
    public DbSet<Project> Projects => Set<Project>();
    public DbSet<TaskItem> Tasks => Set<TaskItem>();

    protected override void OnConfiguring(DbContextOptionsBuilder options) =>
        options.UseSqlite("Data Source=course.db");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Project>().Property(x => x.Name).HasMaxLength(120).IsRequired();
        modelBuilder.Entity<Project>().HasIndex(x => x.Name).IsUnique();
        modelBuilder.Entity<TaskItem>().Property(x => x.Title).HasMaxLength(200).IsRequired();
        modelBuilder.Entity<TaskItem>()
            .HasOne(x => x.Project).WithMany(x => x.Tasks)
            .HasForeignKey(x => x.ProjectId).OnDelete(DeleteBehavior.Restrict);
    }
}

