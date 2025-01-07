import React, { useState } from 'react'
import {
  Box,
  FormControl,
  FormLabel,
  Select,
  Button,
  VStack,
  useToast,
  SimpleGrid,
  useColorModeValue
} from '@chakra-ui/react'
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

  const toast = useToast()
  const bgColor = useColorModeValue('white', 'gray.700')
  const borderColor = useColorModeValue('gray.200', 'gray.600')

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
            <FormLabel>Marka</FormLabel>
            <Select
              name="marka"
              value={formData.marka}
              onChange={handleChange}
              placeholder="Seçiniz"
            >
              {Object.entries(brands).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl>
            <FormLabel>RAM</FormLabel>
            <Select
              name="ram"
              value={formData.ram}
              onChange={handleChange}
              placeholder="Seçiniz"
            >
              {Object.entries(ramOptions).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl>
            <FormLabel>Renk</FormLabel>
            <Select
              name="renk"
              value={formData.renk}
              onChange={handleChange}
              placeholder="Seçiniz"
            >
              {Object.entries(colors).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl>
            <FormLabel>Durum</FormLabel>
            <Select
              name="durum"
              value={formData.durum}
              onChange={handleChange}
              placeholder="Seçiniz"
            >
              {Object.entries(conditions).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
          </FormControl>
        </SimpleGrid>

        <Button
          type="submit"
          colorScheme="blue"
          size="lg"
          width="100%"
          mt={4}
          loadingText="İşlem başlatılıyor..."
        >
          İlanları Getir
        </Button>
      </VStack>
    </Box>
  )
}

export default PhoneForm 