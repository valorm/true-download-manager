import React, { useState } from 'react';
import { Box, Paper, Typography, TextField, Switch, FormControlLabel, Button, Divider } from '@mui/material';

interface SettingsProps {
  onSave: (settings: SettingsData) => void;
  initialSettings?: SettingsData;
}

interface SettingsData {
  maxConcurrentDownloads: number;
  defaultDownloadPath: string;
  useProxy: boolean;
  proxyUrl: string;
  maxBandwidth: number;
  enableNotifications: boolean;
}

const Settings: React.FC<SettingsProps> = ({ onSave, initialSettings }) => {
  const [settings, setSettings] = useState<SettingsData>(initialSettings || {
    maxConcurrentDownloads: 3,
    defaultDownloadPath: '',
    useProxy: false,
    proxyUrl: '',
    maxBandwidth: 0,
    enableNotifications: true
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(settings);
  };

  return (
    <Paper sx={{ p: 3, mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        Download Settings
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          fullWidth
          margin="normal"
          label="Max Concurrent Downloads"
          name="maxConcurrentDownloads"
          type="number"
          value={settings.maxConcurrentDownloads}
          onChange={handleChange}
          inputProps={{ min: 1, max: 10 }}
        />
        <TextField
          fullWidth
          margin="normal"
          label="Default Download Path"
          name="defaultDownloadPath"
          value={settings.defaultDownloadPath}
          onChange={handleChange}
        />
        <TextField
          fullWidth
          margin="normal"
          label="Max Bandwidth (KB/s, 0 for unlimited)"
          name="maxBandwidth"
          type="number"
          value={settings.maxBandwidth}
          onChange={handleChange}
          inputProps={{ min: 0 }}
        />
        <Divider sx={{ my: 2 }} />
        <Typography variant="subtitle1" gutterBottom>
          Proxy Settings
        </Typography>
        <FormControlLabel
          control={
            <Switch
              checked={settings.useProxy}
              onChange={handleChange}
              name="useProxy"
            />
          }
          label="Use Proxy"
        />
        {settings.useProxy && (
          <TextField
            fullWidth
            margin="normal"
            label="Proxy URL"
            name="proxyUrl"
            value={settings.proxyUrl}
            onChange={handleChange}
            placeholder="http://proxy.example.com:8080"
          />
        )}
        <Divider sx={{ my: 2 }} />
        <FormControlLabel
          control={
            <Switch
              checked={settings.enableNotifications}
              onChange={handleChange}
              name="enableNotifications"
            />
          }
          label="Enable Notifications"
        />
        <Box sx={{ mt: 3 }}>
          <Button type="submit" variant="contained" color="primary">
            Save Settings
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default Settings;