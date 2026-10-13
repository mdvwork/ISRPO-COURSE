namespace Course.Core;

public static class ProjectRules
{
    // Намеренная ошибка для демонстрации красного теста.
    public static bool IsNameValid(string? value) =>
        value is null || value.Trim().Length is >= 3 and <= 120;
}

