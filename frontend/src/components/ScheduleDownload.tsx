import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  FormControlLabel,
  Switch,
} from '@mui/material';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider, DateTimePicker } from '@mui/x-date-pickers';

interface ScheduleDownloadProps {
  onSchedule: (scheduleData: ScheduleData) => void;
}

interface ScheduleData {
  url: string;
  scheduledTime: Date | null;
  priority: 'low' | 'medium' | 'high';
  description: string;
  notifyOnComplete: boolean;
}

const ScheduleDownload: React.FC<ScheduleDownloadProps> = ({ onSchedule }) => {
  const [scheduleData, setScheduleData] = useState<ScheduleData>({
    url: '',
    scheduledTime: null,
    priority: 'medium',
    description: '',
    notifyOnComplete: true,
  });

  const handleChange = (field: keyof ScheduleData) => (value: any) => {
    setScheduleData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSchedule(scheduleData);
  };

  return (
    <Paper sx={{ p: 3, mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        Schedule Download
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <Stack spacing={3}>
          <TextField
            fullWidth
            label="URL"
            value={scheduleData.url}
            onChange={(e) => handleChange('url')(e.target.value)}
            placeholder="https://example.com/file.zip"
            required
          />
          
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DateTimePicker
              label="Schedule Time"
              value={scheduleData.scheduledTime}
              onChange={(newValue: Date | null) => handleChange('scheduledTime')(newValue)}
              slotProps={{ textField: { fullWidth: true } }}
            />
          </LocalizationProvider>

          <FormControl fullWidth>
            <InputLabel>Priority</InputLabel>
            <Select
              value={scheduleData.priority}
              label="Priority"
              onChange={(e) => handleChange('priority')(e.target.value)}
            >
              <MenuItem value="low">Low</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="high">High</MenuItem>
            </Select>
          </FormControl>

          <TextField
            fullWidth
            label="Description"
            value={scheduleData.description}
            onChange={(e) => handleChange('description')(e.target.value)}
            multiline
            rows={3}
            placeholder="Add notes about this download"
          />

          <FormControlLabel
            control={
              <Switch
                checked={scheduleData.notifyOnComplete}
                onChange={(e) => handleChange('notifyOnComplete')(e.target.checked)}
              />
            }
            label="Notify when complete"
          />

          <Button type="submit" variant="contained" color="primary">
            Schedule Download
          </Button>
        </Stack>
      </Box>
    </Paper>
  );
};

export default ScheduleDownload;