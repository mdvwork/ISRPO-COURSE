namespace Course.WinForms;

public static class BuggyCalculator
{
    // Намеренная логическая ошибка для ПР 4: при трёх оценках делитель неверен.
    public static double Average(int first, int second, int third) =>
        (first + second + third) / 2.0;
}

