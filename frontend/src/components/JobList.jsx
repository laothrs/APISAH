import { useState, useEffect } from 'react'
import {
  Box,
  VStack,
  Heading,
  Button,
  Text,
  useColorModeValue,
  HStack,
  Flex,
  Badge,
  useToast
} from '@chakra-ui/react'
import { DownloadIcon } from '@chakra-ui/icons'
import axios from 'axios'

function JobList() {
  const [jobs, setJobs] = useState({
    active_jobs: {},
    completed_jobs: {},
    failed_jobs: {}
  })
  const [downloadableJobs, setDownloadableJobs] = useState(new Set())
  const toast = useToast()

  const bgColor = useColorModeValue('white', 'gray.700')
  const borderColor = useColorModeValue('gray.200', 'gray.600')

  const fetchJobs = () => {
    axios.get('http://127.0.0.1:5000/api/jobs')
      .then(response => setJobs(response.data))
      .catch(error => console.error('İşlemler alınamadı:', error))
  }

  const checkFileExists = async (jobId) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/check-file/${jobId}`)
      if (response.data.exists) {
        setDownloadableJobs(prev => new Set([...prev, jobId]))
      }
    } catch (error) {
      console.error('Dosya kontrolü hatası:', error)
    }
  }

  const handleDownload = async (jobId, params) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/download/${jobId}`, {
        responseType: 'blob'
      })
      
      // Dosya adını oluştur
      let fileName = `data_${jobId}.json`
      if (params?.kategori === "Emlak") {
        const folder = params.sehir ? params.sehir : "TumIller"
        fileName = `${folder}_${params.ana_kategori}_${params.durum}.json`
      } else if (params?.kategori === "Cep Telefonu") {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '').slice(0, 15)
        fileName = `${params.marka.toLowerCase()}_${params.durum || 'hepsi'}_${timestamp}.json`
      }
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', fileName)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('İndirme hatası:', error)
      toast({
        title: "İndirme Hatası",
        description: "Dosya indirilemedi. Lütfen tekrar deneyin.",
        status: "error",
        duration: 3000,
        isClosable: true,
      })
    }
  }

  useEffect(() => {
    fetchJobs()
    const interval = setInterval(fetchJobs, 5000)
    return () => clearInterval(interval)
  }, [])

  // Her job güncellemesinde dosya varlığını kontrol et
  useEffect(() => {
    const allJobIds = Object.keys({
      ...jobs.active_jobs,
      ...jobs.completed_jobs,
      ...jobs.failed_jobs
    })
    allJobIds.forEach(jobId => {
      checkFileExists(jobId)
    })
  }, [jobs])

  const getStatusBadge = (jobId) => {
    if (jobs.active_jobs[jobId]) {
      return <Badge colorScheme="yellow">Devam Ediyor</Badge>
    } else if (jobs.completed_jobs[jobId]) {
      return <Badge colorScheme="green">Tamamlandı</Badge>
    } else if (jobs.failed_jobs[jobId]) {
      return <Badge colorScheme="red">Başarısız</Badge>
    }
    return null
  }

  const getJobParams = (jobId) => {
    const job = jobs.active_jobs[jobId] || jobs.completed_jobs[jobId] || jobs.failed_jobs[jobId]
    return job?.params || {}
  }

  const renderJobDetails = (params) => {
    if (params.kategori === "Emlak") {
      return `${params.ana_kategori} - ${params.durum} ${params.sehir ? `- ${params.sehir}` : '- Tüm İller'}`
    } else if (params.kategori === "Cep Telefonu") {
      return `${params.marka} - ${params.sehir}`
    }
    return ''
  }

  return (
    <Box>
      <Heading size="lg" mb={6} textAlign="center">
        İŞLEMLER
      </Heading>
      <VStack spacing={4} align="stretch">
        {Object.entries({...jobs.active_jobs, ...jobs.completed_jobs, ...jobs.failed_jobs})
          .map(([jobId, data]) => {
            const params = getJobParams(jobId)
            return (
              <Box
                key={jobId}
                bg={bgColor}
                borderRadius="lg"
                boxShadow="sm"
                border="1px"
                borderColor={borderColor}
                p={4}
              >
                <Flex align="center" gap={4}>
                  <VStack align="start" flex={1}>
                    <HStack>
                      <Text fontSize="lg" fontWeight="medium">{jobId}</Text>
                      {getStatusBadge(jobId)}
                    </HStack>
                    <Text fontSize="sm" color="gray.500">
                      {renderJobDetails(params)}
                    </Text>
                  </VStack>
                  <Button
                    rightIcon={<DownloadIcon />}
                    colorScheme="blue"
                    variant="outline"
                    size="sm"
                    onClick={() => handleDownload(jobId, params)}
                    isDisabled={!downloadableJobs.has(jobId)}
                  >
                    İNDİR
                  </Button>
                </Flex>
              </Box>
            )
          })}
      </VStack>
    </Box>
  )
}

export default JobList 