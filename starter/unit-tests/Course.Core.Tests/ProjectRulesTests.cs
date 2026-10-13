using Course.Core;

namespace Course.Core.Tests;

[TestClass]
public sealed class ProjectRulesTests
{
    [TestMethod]
    public void IsNameValid_Null_ReturnsFalse() =>
        Assert.IsFalse(ProjectRules.IsNameValid(null));

    [TestMethod]
    public void IsNameValid_NormalName_ReturnsTrue() =>
        Assert.IsTrue(ProjectRules.IsNameValid("Каталог"));
}

