import React from 'react';
import { Box, LinearProgress, Typography, Paper, Grid } from '@mui/material';

interface DownloadProgressProps {
  filename: string;
  progress: number;
  speed: string;
  timeRemaining: string;
  status: 'downloading' | 'paused' | 'completed' | 'error';
}

const DownloadProgress: React.FC<DownloadProgressProps> = ({
  filename,
  progress,
  speed,
  timeRemaining,
  status
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'downloading':
        return 'primary';
      case 'completed':
        return 'success';
      case 'error':
        return 'error';
      default:
        return 'info';
    }
  };

  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="subtitle1" noWrap>
            {filename}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ width: '100%', mr: 1 }}>
              <LinearProgress
                variant="determinate"
                value={progress}
                color={getStatusColor()}
              />
            </Box>
            <Box sx={{ minWidth: 35 }}>
              <Typography variant="body2" color="text.secondary">
                {`${Math.round(progress)}%`}
              </Typography>
            </Box>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <Typography variant="body2" color="text.secondary">
              {speed}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {timeRemaining}
            </Typography>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default DownloadProgress;