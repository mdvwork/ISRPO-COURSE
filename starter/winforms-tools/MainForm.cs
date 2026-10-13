namespace Course.WinForms;

public sealed class MainForm : Form
{
    private readonly TextBox _name = new() { PlaceholderText = "Название проекта", Dock = DockStyle.Top };
    private readonly RadioButton _planned = new() { Text = "Запланирован", Checked = true, AutoSize = true };
    private readonly RadioButton _active = new() { Text = "В работе", AutoSize = true };
    private readonly FlowLayoutPanel _items = new() { Dock = DockStyle.Fill, AutoScroll = true, FlowDirection = FlowDirection.TopDown, WrapContents = false };
    private readonly Label _message = new() { Dock = DockStyle.Bottom, AutoSize = true };
    private int _nextId = 1;

    public MainForm()
    {
        Text = "Учебные проекты";
        Width = 640;
        Height = 480;

        var statuses = new FlowLayoutPanel { Dock = DockStyle.Top, AutoSize = true };
        statuses.Controls.AddRange([_planned, _active]);

        var add = new Button { Text = "Добавить", Dock = DockStyle.Top };
        add.Click += AddProject;

        Controls.Add(_items);
        Controls.Add(_message);
        Controls.Add(add);
        Controls.Add(statuses);
        Controls.Add(_name);
    }

    private void AddProject(object? sender, EventArgs e)
    {
        var name = _name.Text.Trim();
        if (name.Length < 3)
        {
            _message.Text = "Название должно содержать не менее 3 символов.";
            return;
        }

        var project = new ProjectItem(_nextId++, name, _active.Checked ? "В работе" : "Запланирован");
        var row = new Panel { Width = 560, Height = 40, Tag = project };
        var text = new Label { Text = $"{project.Id}. {project.Name} — {project.Status}", AutoSize = true, Left = 4, Top = 10 };
        var remove = new Button { Text = "Удалить", Width = 90, Left = 450, Top = 5 };
        remove.Click += (_, _) => _items.Controls.Remove(row);
        row.Controls.AddRange([text, remove]);
        _items.Controls.Add(row);
        _name.Clear();
        _message.Text = $"Добавлен проект {project.Id}.";
    }
}

