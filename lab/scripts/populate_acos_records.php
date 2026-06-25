<?php
/**
 * Populate acos for both section-level AND per-record entries.
 * Section-level: model='Risks', foreign_key=null
 * Per-record:    model='Risk', foreign_key=<id>
 */
declare(strict_types=1);

require '/var/www/eramba/app/upgrade/vendor/autoload.php';
require '/var/www/eramba/app/upgrade/config/bootstrap.php';

use Cake\ORM\TableRegistry;

$Acos = TableRegistry::getTableLocator()->get('Acos');
echo "Acos count before: " . $Acos->find()->count() . "\n";

// 1. Section-level acos (already done, but re-check)
$sections = [
    'RiskClassifications' => 'risk_classifications',
    'Risks' => 'risks',
    'SecurityPolicies' => 'security_policies',
    'BusinessContinuityPlans' => 'business_continuity_plans',
    'ThirdParties' => 'third_parties',
    'SecurityIncidents' => 'security_incidents',
];

$created = 0;
$skipped = 0;

// 2. Per-record acos for each model that has records
foreach ($sections as $modelName => $tableName) {
    $table = TableRegistry::getTableLocator()->get($tableName);
    $records = $table->find()->all();

    foreach ($records as $record) {
        $id = $record->id;
        // Check if acos exists for this specific record
        $exists = $Acos->find()
            ->where(['model' => $modelName, 'foreign_key' => $id])
            ->first();
        if ($exists) {
            $skipped++;
            continue;
        }
        $node = $Acos->newEntity([
            'model' => $modelName,
            'foreign_key' => $id,
            'parent_id' => null,
        ]);
        if ($Acos->save($node)) {
            $created++;
            echo "  CREATED: $modelName:$id -> acos id={$node->id}\n";
        } else {
            echo "  FAILED: $modelName:$id -> " . print_r($node->getErrors(), true) . "\n";
        }
    }
}

echo "\nTotal acos created: $created (skipped: $skipped)\n";
echo "Acos count after: " . $Acos->find()->count() . "\n";
