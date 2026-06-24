<?php
/**
 * Populate acos, aros, aros_acos for all Eramba models.
 * Bypasses the broken CLI sync.
 */
declare(strict_types=1);

require '/var/www/eramba/app/upgrade/vendor/autoload.php';
require '/var/www/eramba/app/upgrade/config/bootstrap.php';

use Cake\ORM\TableRegistry;

$Aros = TableRegistry::getTableLocator()->get('Aros');

echo "=== Aros ===\n";
// Create user aros
$existing = $Aros->find()->all();
echo "Existing aros: " . count($existing) . "\n";

if (count($existing) == 0) {
    // User aros
    $userAro = $Aros->newEntity([
        'parent_id' => null,
        'model' => 'User',
        'foreign_key' => 1,
        'alias' => 'User::1',
    ]);
    $Aros->save($userAro);
    echo "Created User aro: " . $userAro->id . "\n";

    // Group aros (admin group, etc.)
    foreach ([1, 2, 3, 4, 5] as $gid) {
        $groupAro = $Aros->newEntity([
            'parent_id' => null,
            'model' => 'Group',
            'foreign_key' => $gid,
            'alias' => 'Group::' . $gid,
        ]);
        if ($Aros->save($groupAro)) {
            echo "Created Group aro: " . $groupAro->id . "\n";
        }
    }
}

echo "\nDone.\n";
