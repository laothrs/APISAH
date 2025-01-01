import React, { useState, useEffect } from 'react'
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
import { categories, roomOptions, heatingTypes } from '../data/estateOptions'

function EstateForm() {
  const [formData, setFormData] = useState({
    ana_kategori: '',
    durum: '',
    sehir: '',
    oda_sayisi: '',
    isitma_tipi: ''
  })

  const [durumlar, setDurumlar] = useState({})
  const [showRoomAndHeating, setShowRoomAndHeating] = useState(false)
  
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  })

  useEffect(() => {
    // Ana kategori seçildiğinde durum seçeneklerini güncelle
    if (formData.ana_kategori) {
      setDurumlar(categories[formData.ana_kategori].durumlar)
      setShowRoomAndHeating(['Konut', 'Daire'].includes(formData.ana_kategori))
    } else {
      setDurumlar({})
      setShowRoomAndHeating(false)
    }
  }, [formData.ana_kategori])

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
      const response = await axios.post('http://127.0.0.1:5000/api/scrape/estate', formData)
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
              <InputLabel>Ana Kategori</InputLabel>
              <Select
                name="ana_kategori"
                value={formData.ana_kategori}
                onChange={handleChange}
                label="Ana Kategori"
              >
                <MenuItem value="">
                  <em>Seçiniz</em>
                </MenuItem>
                {Object.keys(categories).map((category) => (
                  <MenuItem key={category} value={category}>
                    {category}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth disabled={!formData.ana_kategori}>
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
                {Object.entries(durumlar).map(([label, value]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

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

          {showRoomAndHeating && (
            <>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Oda Sayısı</InputLabel>
                  <Select
                    name="oda_sayisi"
                    value={formData.oda_sayisi}
                    onChange={handleChange}
                    label="Oda Sayısı"
                  >
                    <MenuItem value="">
                      <em>Seçiniz</em>
                    </MenuItem>
                    {Object.entries(roomOptions).map(([value, label]) => (
                      <MenuItem key={value} value={value}>
                        {label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Isıtma Tipi</InputLabel>
                  <Select
                    name="isitma_tipi"
                    value={formData.isitma_tipi}
                    onChange={handleChange}
                    label="Isıtma Tipi"
                  >
                    <MenuItem value="">
                      <em>Seçiniz</em>
                    </MenuItem>
                    {Object.entries(heatingTypes).map(([value, label]) => (
                      <MenuItem key={value} value={value}>
                        {label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </>
          )}

          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              size="large"
              disabled={!formData.ana_kategori || !formData.durum}
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

export default EstateForm 