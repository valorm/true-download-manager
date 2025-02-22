import React from 'react';
import { Box, Typography, Tabs, Tab, Paper } from '@mui/material';
import DownloadProgress from './DownloadProgress';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

interface Download {
  id: string;
  filename: string;
  progress: number;
  speed: string;
  timeRemaining: string;
  status: 'downloading' | 'paused' | 'completed' | 'error';
  createdAt: string;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`download-tabpanel-${index}`}
      aria-labelledby={`download-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const DownloadHistory: React.FC = () => {
  const [value, setValue] = React.useState(0);
  const [downloads] = React.useState<Download[]>([]); // This will be replaced with actual data

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const activeDownloads = downloads.filter(d => d.status === 'downloading' || d.status === 'paused');
  const completedDownloads = downloads.filter(d => d.status === 'completed');
  const failedDownloads = downloads.filter(d => d.status === 'error');

  return (
    <Paper sx={{ width: '100%', mt: 2 }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="download history tabs">
          <Tab label={`Active (${activeDownloads.length})`} />
          <Tab label={`Completed (${completedDownloads.length})`} />
          <Tab label={`Failed (${failedDownloads.length})`} />
        </Tabs>
      </Box>

      <TabPanel value={value} index={0}>
        {activeDownloads.length === 0 ? (
          <Typography>No active downloads</Typography>
        ) : (
          activeDownloads.map(download => (
            <DownloadProgress
              key={download.id}
              filename={download.filename}
              progress={download.progress}
              speed={download.speed}
              timeRemaining={download.timeRemaining}
              status={download.status}
            />
          ))
        )}
      </TabPanel>

      <TabPanel value={value} index={1}>
        {completedDownloads.length === 0 ? (
          <Typography>No completed downloads</Typography>
        ) : (
          completedDownloads.map(download => (
            <DownloadProgress
              key={download.id}
              filename={download.filename}
              progress={100}
              speed="-"
              timeRemaining="-"
              status={download.status}
            />
          ))
        )}
      </TabPanel>

      <TabPanel value={value} index={2}>
        {failedDownloads.length === 0 ? (
          <Typography>No failed downloads</Typography>
        ) : (
          failedDownloads.map(download => (
            <DownloadProgress
              key={download.id}
              filename={download.filename}
              progress={download.progress}
              speed="-"
              timeRemaining="-"
              status={download.status}
            />
          ))
        )}
      </TabPanel>
    </Paper>
  );
};

export default DownloadHistory;