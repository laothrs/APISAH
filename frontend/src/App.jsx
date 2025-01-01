import { useState } from 'react'
import { Container, Box, Typography, Paper, Tabs, Tab } from '@mui/material'
import PhoneForm from './components/PhoneForm'
import EstateForm from './components/EstateForm'
import JobList from './components/JobList'

function App() {
  const [activeTab, setActiveTab] = useState(0)

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue)
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Sahibinden.com Veri Çekme Aracı
      </Typography>

      <Paper sx={{ mb: 4 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          centered
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab label="Cep Telefonu" />
          <Tab label="Emlak" />
          <Tab label="İşlemler" />
        </Tabs>
      </Paper>

      <Box sx={{ mt: 2 }}>
        {activeTab === 0 && <PhoneForm />}
        {activeTab === 1 && <EstateForm />}
        {activeTab === 2 && <JobList />}
      </Box>
    </Container>
  )
}

export default App
