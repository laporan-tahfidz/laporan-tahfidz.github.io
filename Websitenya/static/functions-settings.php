<?php
require_once __DIR__ . '/library/rb-sqlite.php';

/**
 * Get a setting value by key from the database
 * 
 * @param string $key The setting key
 * @return string|null The setting value or null if not found
 */
function getSetting($key) {
    try {
        $setting = R::findOne('settings', 'key = ?', [$key]);
        return $setting ? $setting->value : null;
    } catch (Exception $e) {
        error_log("Error getting setting: " . $e->getMessage());
        return null;
    }
}

/**
 * Set a setting value by key in the database
 * 
 * @param string $key The setting key
 * @param string $value The setting value
 * @return bool True on success, false on failure
 */
function setSetting($key, $value) {
    try {
        $setting = R::findOne('settings', 'key = ?', [$key]);
        
        if (!$setting) {
            // Create new setting
            $setting = R::dispense('settings');
            $setting->key = $key;
        }
        
        $setting->value = $value;
        $setting->updated_at = R::isoDateTime();
        R::store($setting);
        
        return true;
    } catch (Exception $e) {
        error_log("Error setting setting: " . $e->getMessage());
        return false;
    }
}

/**
 * Get the selected WhatsApp group ID from the database
 * 
 * @return string|null The selected group ID or null if not set
 */
function getSelectedWhatsAppGroupId() {
    return getSetting('whatsapp_group_id');
}

/**
 * Set the selected WhatsApp group ID in the database
 * 
 * @param string $groupId The group ID to save
 * @return bool True on success, false on failure
 */
function setSelectedWhatsAppGroupId($groupId) {
    return setSetting('whatsapp_group_id', $groupId);
}
?>