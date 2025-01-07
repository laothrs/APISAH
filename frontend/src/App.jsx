import { useState } from 'react'
import {
  Box,
  Container,
  Grid,
  GridItem,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Heading,
  useColorMode,
  Button,
  Flex,
  Icon,
  Text,
  Link,
  VStack
} from '@chakra-ui/react'
import { SunIcon, MoonIcon } from '@chakra-ui/icons'
import PhoneForm from './components/PhoneForm'
import EstateForm from './components/EstateForm'
import JobList from './components/JobList'

function App() {
  const { colorMode, toggleColorMode } = useColorMode()

  return (
    <Box minH="100vh" bg={colorMode === 'light' ? 'gray.50' : 'gray.800'} p={4}>
      <Grid
        templateColumns="250px 1fr"
        gap={4}
        maxW="container.xl"
        mx="auto"
      >
        {/* Sol Sidebar - Özellikler */}
        <GridItem>
          <Box
            bg={colorMode === 'light' ? 'white' : 'gray.700'}
            borderRadius="lg"
            boxShadow="base"
            p={4}
            height="full"
          >
            <Heading size="md" mb={4}>ÖZELLİKLER</Heading>
            <VStack align="stretch" spacing={3}>
              <Text>• Tüm illeri otomatik tarama</Text>
              <Text>• Her il için 50 sayfa veri</Text>
              <Text>• Cloudflare bypass desteği</Text>
              <Text>• Bot tespiti engelleme</Text>
              <Text>• Asenkron veri çekme</Text>
              <Text>• İşlem takip sistemi</Text>
              <Text>• Otomatik veri kaydetme</Text>
              <Text>• Detaylı filtreleme</Text>
            </VStack>
          </Box>
        </GridItem>

        {/* Ana İçerik */}
        <GridItem>
          <VStack spacing={4} align="stretch">
            {/* Ana Panel */}
            <Box
              bg={colorMode === 'light' ? 'white' : 'gray.700'}
              borderRadius="lg"
              boxShadow="base"
              overflow="hidden"
              p={4}
              flex="1"
            >
              <Flex justify="space-between" align="center" mb={4}>
                <Heading
                  size="lg"
                  bgGradient="linear(to-r, blue.400, teal.400)"
                  bgClip="text"
                >
                  TEMEL API SİSTEMİ
                </Heading>
                <Button
                  onClick={toggleColorMode}
                  size="md"
                  variant="ghost"
                  _hover={{ bg: colorMode === 'light' ? 'gray.100' : 'gray.700' }}
                >
                  <Icon
                    as={colorMode === 'light' ? MoonIcon : SunIcon}
                    color={colorMode === 'light' ? 'gray.600' : 'gray.400'}
                  />
                </Button>
              </Flex>

              <Tabs isFitted variant="enclosed" colorScheme="blue">
                <TabList>
                  <Tab
                    _selected={{
                      color: 'blue.500',
                      borderColor: 'blue.500',
                      borderBottom: '2px solid'
                    }}
                  >
                    Cep Telefonu
                  </Tab>
                  <Tab
                    _selected={{
                      color: 'blue.500',
                      borderColor: 'blue.500',
                      borderBottom: '2px solid'
                    }}
                  >
                    Emlak
                  </Tab>
                  <Tab
                    _selected={{
                      color: 'blue.500',
                      borderColor: 'blue.500',
                      borderBottom: '2px solid'
                    }}
                  >
                    İşlemler
                  </Tab>
                </TabList>

                <TabPanels>
                  <TabPanel>
                    <PhoneForm />
                  </TabPanel>
                  <TabPanel>
                    <EstateForm />
                  </TabPanel>
                  <TabPanel>
                    <JobList />
                  </TabPanel>
                </TabPanels>
              </Tabs>
            </Box>

            {/* Alt Bilgi Kutuları */}
            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
              <Box
                bg={colorMode === 'light' ? 'white' : 'gray.700'}
                borderRadius="lg"
                boxShadow="base"
                p={4}
                textAlign="center"
              >
                <Link href="https://t.me/Laothz" isExternal color="blue.500">
                  t.me/Laothz
                </Link>
              </Box>
              <Box
                bg={colorMode === 'light' ? 'white' : 'gray.700'}
                borderRadius="lg"
                boxShadow="base"
                p={4}
                textAlign="center"
              >
                <Text>İletişim Telegram üzerindendir.</Text>
              </Box>
            </Grid>
          </VStack>
        </GridItem>
      </Grid>
    </Box>
  )
}

export default App
