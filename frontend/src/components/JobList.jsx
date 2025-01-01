import { useState, useEffect } from 'react'
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Chip,
  IconButton,
  Box,
  Collapse,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  ListItemText
} from '@mui/material'
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown'
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp'
import axios from 'axios'

function Row({ job_id, data }) {
  const [open, setOpen] = useState(false)
  const [details, setDetails] = useState(null)
  const [selectedFields, setSelectedFields] = useState(['baslik', 'fiyat', 'konum', 'tarih', 'metrekare', 'oda_sayisi', 'isitma_tipi', 'kat_sayisi', 'bina_yasi'])

  useEffect(() => {
    if (open && !details) {
      axios.get(`http://127.0.0.1:5000/api/status/${job_id}`)
        .then(response => setDetails(response.data))
        .catch(error => console.error('Detaylar alınamadı:', error))
    }
  }, [open, job_id, details])

  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'primary'
      case 'completed':
        return 'success'
      case 'failed':
        return 'error'
      default:
        return 'default'
    }
  }

  const formatDate = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString('tr-TR')
  }

  const handleFieldChange = (event) => {
    setSelectedFields(event.target.value)
  }

  const fieldLabels = {
    baslik: 'İlan Başlığı',
    fiyat: 'Fiyat',
    konum: 'Konum',
    tarih: 'İlan Tarihi',
    metrekare: 'Metrekare',
    oda_sayisi: 'Oda Sayısı',
    isitma_tipi: 'Isıtma Tipi',
    kat_sayisi: 'Kat',
    bina_yasi: 'Bina Yaşı'
  }

  return (
    <>
      <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {job_id}
        </TableCell>
        <TableCell>
          <Chip
            label={data.status}
            color={getStatusColor(data.status)}
            size="small"
          />
        </TableCell>
        <TableCell>{data.params?.kategori || '-'}</TableCell>
        <TableCell>{formatDate(data.start_time)}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Typography variant="h6" gutterBottom component="div">
                Detaylar
              </Typography>
              {details && (
                <>
                  <Typography variant="body2" gutterBottom>
                    Durum: {details.status}
                  </Typography>
                  {details.total_items && (
                    <Typography variant="body2" gutterBottom>
                      Toplam İlan: {details.total_items}
                    </Typography>
                  )}
                  {details.error && (
                    <Typography variant="body2" color="error" gutterBottom>
                      Hata: {details.error}
                    </Typography>
                  )}
                  <FormControl sx={{ m: 1, minWidth: 200 }}>
                    <InputLabel>Gösterilecek Alanlar</InputLabel>
                    <Select
                      multiple
                      value={selectedFields}
                      onChange={handleFieldChange}
                      renderValue={(selected) => selected.map(field => fieldLabels[field]).join(', ')}
                    >
                      {Object.entries(fieldLabels).map(([field, label]) => (
                        <MenuItem key={field} value={field}>
                          <Checkbox checked={selectedFields.includes(field)} />
                          <ListItemText primary={label} />
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <Typography variant="subtitle2" gutterBottom>
                    İlan Detayları:
                  </Typography>
                  {details.items && details.items.map((item, index) => (
                    <Box key={index} sx={{ mb: 1, p: 1, bgcolor: '#f5f5f5' }}>
                      {selectedFields.map(field => (
                        <Typography key={field} variant="body2">
                          {fieldLabels[field]}: {item[field]}
                        </Typography>
                      ))}
                    </Box>
                  ))}
                </>
              )}
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  )
}

function JobList() {
  const [jobs, setJobs] = useState({
    active_jobs: {},
    completed_jobs: {},
    failed_jobs: {}
  })

  const fetchJobs = () => {
    axios.get('http://127.0.0.1:5000/api/jobs')
      .then(response => setJobs(response.data))
      .catch(error => console.error('İşlemler alınamadı:', error))
  }

  useEffect(() => {
    fetchJobs()
    const interval = setInterval(fetchJobs, 5000)  // Her 5 saniyede bir güncelle
    return () => clearInterval(interval)
  }, [])

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6" component="div">
          İşlem Listesi
        </Typography>
        <Button onClick={fetchJobs} variant="outlined" size="small">
          Yenile
        </Button>
      </Box>
      
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="işlem listesi">
          <TableHead>
            <TableRow>
              <TableCell />
              <TableCell>İşlem ID</TableCell>
              <TableCell>Durum</TableCell>
              <TableCell>Kategori</TableCell>
              <TableCell>Başlangıç</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {/* Aktif İşlemler */}
            {Object.entries(jobs.active_jobs).map(([job_id, data]) => (
              <Row key={job_id} job_id={job_id} data={data} />
            ))}
            
            {/* Tamamlanan İşlemler */}
            {Object.entries(jobs.completed_jobs).map(([job_id, data]) => (
              <Row key={job_id} job_id={job_id} data={data} />
            ))}
            
            {/* Başarısız İşlemler */}
            {Object.entries(jobs.failed_jobs).map(([job_id, data]) => (
              <Row key={job_id} job_id={job_id} data={data} />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  )
}

export default JobList 