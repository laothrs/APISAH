import React, { useState } from 'react'
import {
  Paper,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Snackbar,
  Alert
} from '@mui/material'
import axios from 'axios'
import { cities } from '../data/cities'
import { brands, ramOptions, colors, conditions } from '../data/phoneOptions'

function PhoneForm() {
  const [formData, setFormData] = useState({
    sehir: '',
    marka: '',
    ram: '',
    renk: '',
    durum: ''
  })
  
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  })

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/scrape/phone', formData)
      setSnackbar({
        open: true,
        message: `İşlem başlatıldı! İşlem ID: ${response.data.job_id}`,
        severity: 'success'
      })
    } catch (error) {
      setSnackbar({
        open: true,
        message: 'Bir hata oluştu: ' + error.message,
        severity: 'error'
      })
    }
  }

  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }))
  }

  return (
    <Paper sx={{ p: 3 }}>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Şehir</InputLabel>
              <Select
                name="sehir"
                value={formData.sehir}
                onChange={handleChange}
                label="Şehir"
              >
                <MenuItem value="">
                  <em>Seçiniz</em>
                </MenuItem>
                {Object.entries(cities).map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Marka</InputLabel>
              <Select
                name="marka"
                value={formData.marka}
                onChange={handleChange}
                label="Marka"
              >
                <MenuItem value="">
                  <em>Seçiniz</em>
                </MenuItem>
                {Object.entries(brands).map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>RAM</InputLabel>
              <Select
                name="ram"
                value={formData.ram}
                onChange={handleChange}
                label="RAM"
              >
                <MenuItem value="">
                  <em>Seçiniz</em>
                </MenuItem>
                {Object.entries(ramOptions).map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Renk</InputLabel>
              <Select
                name="renk"
                value={formData.renk}
                onChange={handleChange}
                label="Renk"
              >
                <MenuItem value="">
                  <em>Seçiniz</em>
                </MenuItem>
                {Object.entries(colors).map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Durum</InputLabel>
              <Select
                name="durum"
                value={formData.durum}
                onChange={handleChange}
                label="Durum"
              >
                <MenuItem value="">
                  <em>Seçiniz</em>
                </MenuItem>
                {Object.entries(conditions).map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              size="large"
            >
              İlanları Getir
            </Button>
          </Grid>
        </Grid>
      </form>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Paper>
  )
}

export default PhoneForm 