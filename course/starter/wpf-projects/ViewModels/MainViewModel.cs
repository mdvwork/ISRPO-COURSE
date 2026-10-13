using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Course.Wpf.Models;

namespace Course.Wpf.ViewModels;

public sealed class MainViewModel : INotifyPropertyChanged
{
    private string _draftName = string.Empty;
    private ProjectItem? _selectedProject;
    private int _nextId = 3;

    public ObservableCollection<ProjectItem> Projects { get; } =
    [
        new() { Id = 1, Name = "Каталог", Hours = 12 },
        new() { Id = 2, Name = "Трекер", Hours = 8 }
    ];

    public string DraftName
    {
        get => _draftName;
        set { _draftName = value; OnPropertyChanged(); AddCommand.RaiseCanExecuteChanged(); }
    }

    public ProjectItem? SelectedProject
    {
        get => _selectedProject;
        set { _selectedProject = value; OnPropertyChanged(); DeleteCommand.RaiseCanExecuteChanged(); }
    }

    public RelayCommand AddCommand { get; }
    public RelayCommand DeleteCommand { get; }

    public MainViewModel()
    {
        AddCommand = new RelayCommand(Add, () => DraftName.Trim().Length >= 3);
        DeleteCommand = new RelayCommand(Delete, () => SelectedProject is not null);
    }

    private void Add()
    {
        Projects.Add(new ProjectItem { Id = _nextId++, Name = DraftName.Trim(), Hours = 0 });
        DraftName = string.Empty;
    }

    private void Delete()
    {
        if (SelectedProject is not null)
            Projects.Remove(SelectedProject);
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    private void OnPropertyChanged([CallerMemberName] string? name = null) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}

