<?php
declare(strict_types=1);
require dirname(__DIR__) . '/src/bootstrap.php';

$stmt = $pdo->query('SELECT id, name, hours, status FROM projects ORDER BY name');
$projects = $stmt->fetchAll();
?>
<!doctype html><html lang="ru"><meta charset="utf-8"><title>Проекты</title>
<h1>Проекты</h1>
<?php if (!$projects): ?><p>Проектов пока нет.</p><?php endif; ?>
<?php foreach ($projects as $project): ?>
  <article><h2><?= h($project['name']) ?></h2>
    <p><?= (int)$project['hours'] ?> ч. — <?= h($project['status']) ?></p></article>
<?php endforeach; ?></html>

