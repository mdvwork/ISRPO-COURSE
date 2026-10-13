using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace Course.Wpf.Models;

public sealed class ProjectItem : INotifyPropertyChanged
{
    private string _name = string.Empty;
    private int _hours;

    public int Id { get; init; }
    public string Name { get => _name; set { _name = value; OnPropertyChanged(); } }
    public int Hours { get => _hours; set { _hours = value; OnPropertyChanged(); } }

    public event PropertyChangedEventHandler? PropertyChanged;
    private void OnPropertyChanged([CallerMemberName] string? name = null) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}

