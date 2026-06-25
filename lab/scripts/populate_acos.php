<?php
/**
 * Direct acos population script.
 * Bypasses the broken access_control sync command by writing acos entries directly.
 * Run: php /tmp/populate_acos.php
 */
declare(strict_types=1);

require '/var/www/eramba/app/upgrade/vendor/autoload.php';
require '/var/www/eramba/app/upgrade/config/bootstrap.php';

use Cake\Datasource\FactoryLocator;
use Cake\ORM\TableRegistry;

$now = date('Y-m-d H:i:s');

// Resolve the Acos table via the AccessControl plugin's AccessControlManagerBehavior
// The Acos table is just a Cake table — we use TableRegistry

$Acos = TableRegistry::getTableLocator()->get('Acos');
$Authorizations = TableRegistry::getTableLocator()->get('Authorizations');

// Get all authorization IDs by model
$authRows = $Authorizations->find('all')->all();
echo "Found " . count($authRows) . " authorizations\n";

foreach ($authRows as $auth) {
    $model = $auth->model;
    $foreignKey = $auth->foreign_key;

    // Check if acos entry exists
    $existing = $Acos->find()
        ->where(['model' => $model])
        ->where(function ($exp) use ($foreignKey) {
            if ($foreignKey === null) {
                return $exp->isNull('foreign_key');
            }
            return $exp->eq('foreign_key', $foreignKey);
        })
        ->first();

    if ($existing) {
        echo "  EXISTS: $model ($foreignKey) -> acos id={$existing->id}\n";
        continue;
    }

    // Create new acos
    $node = $Acos->newEntity([
        'model' => $model,
        'foreign_key' => $foreignKey,
        'parent_id' => null,
    ]);
    if ($Acos->save($node)) {
        echo "  CREATED: $model ($foreignKey) -> acos id={$node->id}\n";
    } else {
        echo "  FAILED: $model ($foreignKey) -> errors: " . print_r($node->getErrors(), true) . "\n";
    }
}

echo "\nDone.\n";
