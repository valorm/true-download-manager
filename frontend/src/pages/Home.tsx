import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const Home: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Download Manager Dashboard
        </Typography>
        {/* Download components will be added here */}
      </Box>
    </Container>
  );
};

export default Home;