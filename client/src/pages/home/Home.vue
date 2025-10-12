<script setup>
  import { useRouter } from 'vue-router'
const router = useRouter()
 const checks = ["Zero Hassle.", "One Platform.", "Instant Resolution."]
</script>
<template>
<header class="flex flex-col gap-8 pt-8 md:pt-16 lg:pt-24 items-center justify-center px-4">
  <div>
    <svg class="w-24 h-12 md:w-32 md:h-16 lg:w-40 lg:h-20" viewBox="0 0 133 68" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M125.397 20.3777C124.527 20.3777 123.691 20.5432 122.918 20.8341V18.8545C122.918 8.4432 114.502 0 104.123 0H28.8654C18.4872 0 10.0765 8.4432 10.0765 18.8545V20.8341C9.30306 20.5432 8.47286 20.3777 7.59706 20.3777C3.67896 20.3777 0.5 23.5 0.500061 27.4974L1 30L3.00006 31.5L6 33L9.50006 33.5L3.00006 36L0.500061 39.8769C0.500061 43.8076 3.67896 46.9966 7.59706 46.9966C8.46716 46.9966 9.30306 46.8311 10.0765 46.5402V48.5198C10.0765 58.9309 18.4929 67.3739 28.8711 67.3739H104.129C114.507 67.3739 122.924 58.9309 122.924 48.5198V46.5402C123.697 46.8311 124.527 46.9966 125.403 46.9966C129.321 46.9966 132.5 45.5 132.5 39.8769L129 37L124 36L129 33L131 30C132.078 26.5026 129.321 20.3777 125.403 20.3777H125.397Z" fill="#E32958"/>
      <path d="M91.1691 12.3623H41.8254C30.0855 12.3623 20.5685 21.9097 20.5685 33.687V33.6927C20.5685 45.4701 30.0855 55.0179 41.8254 55.0179H91.1691C102.909 55.0179 112.426 45.4701 112.426 33.6927V33.687C112.426 21.9097 102.909 12.3623 91.1691 12.3623Z" fill="white"/>
      <path d="M45.3001 43.2883C48.6889 43.2883 51.4361 39.5414 51.4361 34.9193C51.4361 30.2972 48.6889 26.5503 45.3001 26.5503C41.9113 26.5503 39.1642 30.2972 39.1642 34.9193C39.1642 39.5414 41.9113 43.2883 45.3001 43.2883Z" fill="#111111"/>
      <path d="M87.6951 43.2883C91.0831 43.2883 93.8311 39.5414 93.8311 34.9193C93.8311 30.2972 91.0831 26.5503 87.6951 26.5503C84.3059 26.5503 81.5587 30.2972 81.5587 34.9193C81.5587 39.5414 84.3059 43.2883 87.6951 43.2883Z" fill="#111111"/>
    </svg>
  </div>

  <div class="flex flex-col items-center justify-center gap-2 md:gap-3 lg:gap-4">
    <h3 class="text-xl md:text-2xl lg:text-3xl xl:text-4xl font-extrabold text-center">
      Resolution to All Your Problems <span class="font-mali">?</span>
    </h3>
    <h2 class="font-display text-lg md:text-xl lg:text-2xl xl:text-3xl text-[#196062]">IN ONE PLACE</h2>
  </div>

  <!-- Checks: Column on mobile, Row on desktop -->
  <div class="flex flex-col md:flex-row gap-4 md:gap-6 lg:gap-8">
    <p v-for="check in checks" :key="check" class="flex flex-row gap-2 items-center font-bold text-sm md:text-base lg:text-lg">
      <svg class="w-5 h-5 md:w-6 md:h-6 flex-shrink-0" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3.42857 0.373901C2.51926 0.373901 1.64719 0.735125 1.00421 1.37811C0.361223 2.02109 0 2.89316 0 3.80247V20.9453C0 21.8546 0.361223 22.7267 1.00421 23.3697C1.64719 24.0127 2.51926 24.3739 3.42857 24.3739H20.5714C21.4807 24.3739 22.3528 24.0127 22.9958 23.3697C23.6388 22.7267 24 21.8546 24 20.9453V3.80247C24 2.89316 23.6388 2.02109 22.9958 1.37811C22.3528 0.735125 21.4807 0.373901 20.5714 0.373901H3.42857ZM10.2857 18.2265L5.64514 13.5859L8.06914 11.1619L10.2857 13.3785L16.788 6.87619L19.212 9.30019L10.2857 18.2265Z" fill="black"/>
      </svg>
      {{ check }}
    </p>
  </div>

  <div class="flex flex-col sm:flex-row gap-4 items-center">
    <button @click="router.push('/chatbot')" class="bg-[#196062] text-white font-semibold! rounded-md px-6 py-3 text-sm md:text-base lg:text-lg hover:bg-[#145052] transition-colors w-full sm:w-auto">
      Raise Issue
    </button>
    <div class="hidden sm:block h-12 w-px bg-gray-300"></div>
    <button @click="router.push('/employee/login')" class="border-[#196062] border-2 text-black font-semibold! rounded-md px-6 py-3 text-sm md:text-base lg:text-lg hover:bg-[#196062] hover:text-white transition-colors w-full sm:w-auto">
      Employee Login
    </button>
  </div>
</header>
</template>
