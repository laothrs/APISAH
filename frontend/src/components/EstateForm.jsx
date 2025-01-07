import React, { useState, useEffect } from 'react'
import {
  Box,
  FormControl,
  FormLabel,
  Select,
  Button,
  VStack,
  useToast,
  SimpleGrid,
  Checkbox,
  useColorModeValue
} from '@chakra-ui/react'
import axios from 'axios'
import { cities } from '../data/cities'
import { categories, roomOptions, heatingTypes } from '../data/estateOptions'

function EstateForm() {
  const [formData, setFormData] = useState({
    ana_kategori: '',
    durum: '',
    sehir: '',
    oda_sayisi: '',
    isitma_tipi: '',
    tum_iller: false
  })

  const [durumlar, setDurumlar] = useState({})
  const [showRoomAndHeating, setShowRoomAndHeating] = useState(false)

  const toast = useToast()
  const bgColor = useColorModeValue('white', 'gray.700')
  const borderColor = useColorModeValue('gray.200', 'gray.600')

  useEffect(() => {
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
      const requestData = {
        ana_kategori: formData.ana_kategori,
        durum: formData.durum,
        sehir: formData.tum_iller ? null : formData.sehir,
        oda_sayisi: formData.oda_sayisi,
        isitma_tipi: formData.isitma_tipi,
        tum_iller: formData.tum_iller
      }

      const response = await axios.post('http://127.0.0.1:5000/api/scrape/estate', requestData)
      toast({
        title: 'İşlem Başlatıldı',
        description: `İşlem ID: ${response.data.job_id}`,
        status: 'success',
        duration: 5000,
        isClosable: true,
        position: 'top-right'
      })
    } catch (error) {
      toast({
        title: 'Hata',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
        position: 'top-right'
      })
    }
  }

  return (
    <Box
      as="form"
      onSubmit={handleSubmit}
      bg={bgColor}
      p={6}
      borderRadius="lg"
      boxShadow="sm"
      border="1px"
      borderColor={borderColor}
    >
      <VStack spacing={6}>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} width="100%">
          <FormControl>
            <FormLabel>Ana Kategori</FormLabel>
            <Select
              name="ana_kategori"
              value={formData.ana_kategori}
              onChange={handleChange}
              placeholder="Seçiniz"
            >
              {Object.keys(categories).map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl isDisabled={!formData.ana_kategori}>
            <FormLabel>Durum</FormLabel>
            <Select
              name="durum"
              value={formData.durum}
              onChange={handleChange}
              placeholder="Seçiniz"
            >
              {Object.entries(durumlar).map(([label, value]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl isDisabled={formData.tum_iller}>
            <FormLabel>Şehir</FormLabel>
            <Select
              name="sehir"
              value={formData.sehir}
              onChange={handleChange}
              placeholder="Seçiniz"
            >
              {Object.entries(cities).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl>
            <Checkbox
              mt={8}
              isChecked={formData.tum_iller}
              onChange={(e) => {
                setFormData(prev => ({
                  ...prev,
                  tum_iller: e.target.checked,
                  sehir: e.target.checked ? '' : prev.sehir
                }))
              }}
            >
              Tüm illeri tara (Ankara'dan başlayarak)
            </Checkbox>
          </FormControl>

          {showRoomAndHeating && (
            <>
              <FormControl>
                <FormLabel>Oda Sayısı</FormLabel>
                <Select
                  name="oda_sayisi"
                  value={formData.oda_sayisi}
                  onChange={handleChange}
                  placeholder="Seçiniz"
                >
                  {Object.entries(roomOptions).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </Select>
              </FormControl>

              <FormControl>
                <FormLabel>Isıtma Tipi</FormLabel>
                <Select
                  name="isitma_tipi"
                  value={formData.isitma_tipi}
                  onChange={handleChange}
                  placeholder="Seçiniz"
                >
                  {Object.entries(heatingTypes).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </Select>
              </FormControl>
            </>
          )}
        </SimpleGrid>

        <Button
          type="submit"
          colorScheme="blue"
          size="lg"
          width="100%"
          mt={4}
          isDisabled={!formData.ana_kategori || !formData.durum}
          loadingText="İşlem başlatılıyor..."
        >
          İlanları Getir
        </Button>
      </VStack>
    </Box>
  )
}

export default EstateForm 