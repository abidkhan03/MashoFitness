window.alpine_data = {
  isSideMenuOpen: false,
  toggleSideMenu() {
    this.isSideMenuOpen = !this.isSideMenuOpen;
  },
  closeSideMenu() {
    this.isSideMenuOpen = false;
  },
  isNotificationsMenuOpen: false,
  toggleNotificationsMenu() {
    this.isNotificationsMenuOpen = !this.isNotificationsMenuOpen
    console.log("notifications menu")
    get_all_member_remaining_expiredays()
  },
  closeNotificationsMenu() {
    this.isNotificationsMenuOpen = false;
  },
  // header setting
  isSettingOpen: false,
  toggleSettingMenu() {
    this.isSettingOpen = !this.isSettingOpen;
  },
  closeSettingMenu() {
    this.isSettingOpen = false;
  },
  // header Profile
  isProfileMenuOpen: false,
  toggleProfileMenu() {
    this.isProfileMenuOpen = !this.isProfileMenuOpen;
  },
  closeProfileMenu() {
    this.isProfileMenuOpen = false;
  },
  isGymMemberMenuOpen: false,
  toggleGymMemberMenu() {
    this.isGymMemberMenuOpen = !this.isGymMemberMenuOpen;
  },
  isSettingsMenuOpen: false,
  toggleSettingsMenu() {
    this.isSettingsMenuOpen = !this.isSettingsMenuOpen;
  },
  // futsal
  isFutsalMenuOpen: false,
  toggleFutsalMenu() {
    this.isFutsalMenuOpen = !this.isFutsalMenuOpen;
  },
  // Reports
  isReportsMenuOpen: false,
  toggleReportsMenu() {
    this.isReportsMenuOpen = !this.isReportsMenuOpen;
  },
  // Accountings
  isAccountingMenuOpen: false,
  toggleAccountingMenu() {
    this.isAccountingMenuOpen = !this.isAccountingMenuOpen;
  },
  // Items
  isItemsMenuOpen: false,
  toggleItemsMenu() {
    this.isItemsMenuOpen = !this.isItemsMenuOpen;
  },
  // Orders
  isOrdersMenuOpen: false,
  toggleOrdersMenu() {
    this.isOrdersMenuOpen = !this.isOrdersMenuOpen;
  },
  // Purchases
  isPurchasesMenuOpen: false,
  togglePurchasesMenu() {
    this.isPurchasesMenuOpen = !this.isPurchasesMenuOpen;
  },
  // Sales
  isSalesMenuOpen: false,
  toggleSalesMenu() {
    this.isSalesMenuOpen = !this.isSalesMenuOpen;
  },
  // Modal
  isModalOpen: false,
  trapCleanup: null,
  openModal() {
    // if(window.add_array.length > 0) {
    
    // if(call==''){
    //   alert("Please select a row")
    // }
    // else{
    // console.log("open modal", call)
    this.isModalOpen = true;
    this.trapCleanup = focusTrap(document.querySelector('#modal'));
    // if (call == "inventory") {
    //   console.log("inventory")
    //   inventory_query_call_nonstock()
    // }
    // else {
      console.log("member")
      addInventoryItem()
    // }
    // }
    // else{
    //   alert("Please select a row")
    // }
  },
  closeModal() {
    this.isModalOpen = false;
    this.trapCleanup();
  },

  // Modal
  isUpdateModalOpen: false,
  trapCleanup222: null,
  openUpdateModal(id, call) {
    this.isUpdateModalOpen = true;
    this.trapCleanup222 = focusTrap(document.querySelector('#updateModal'));
    if (call == "non_stock") {
      update_query_call_nonstock(id)
    }
    else if (call == "stock") {
      update_query_call(id)
    }
    else if (call == "inventory") {
      update_query_call_inventory(id)
    }


  },
  closeUpdateModal() {
    this.isUpdateModalOpen = false;
    this.trapCleanup222();
  },

  // Product Modal
  isProductModalOpen: false,
  trapCleanup1: null,
  openProductModal() {
    this.isProductModalOpen = true
    this.trapCleanup1 = focusTrap(document.querySelector('#productModal'))
  },
  closeProductModal() {
    this.isProductModalOpen = false
    this.trapCleanup1()
  },

  // Inventory Sub Modal
  isSubModalOpen: false,
  trapCleanup2: null,
  openSubModal() {
    this.isSubModalOpen = true
    this.trapCleanup2 = focusTrap(document.querySelector('#SubModal'))
  },
  closeSubModal() {
    this.isSubModalOpen = false
    this.trapCleanup2()
  },

  // SMS Modal
  isSMSModalOpen: false,
  trapCleanupSMS: null,
  openSMSModal(ids) {
    this.isSMSModalOpen = true
    this.trapCleanupSMS = focusTrap(document.querySelector('#SMSModal'))
    set_member_id(ids)

  },
  closeSMSModal() {
    this.isSMSModalOpen = false
    this.trapCleanupSMS()
  },

  // View Bill Modal
  isViewBillModalOpen: false,
  trapCleanupViewBill: null,
  openViewBillModal(id) {

    this.isViewBillModalOpen = true
    this.trapCleanupViewBill = focusTrap(document.querySelector('#ViewBillModal'))
    console.log(id)
    ViewBillCall(id)
  },
  closeViewBillModal() {
    this.isViewBillModalOpen = false
    this.trapCleanupViewBill()
  },

  // View ALL Sms Modal
  isViewAllSmsModalOpen: false,
  trapCleanupViewAllSms: null,
  openViewAllSmsModal() {

    this.isViewAllSmsModalOpen = true
    this.trapCleanupViewAllSms = focusTrap(document.querySelector('#ViewAllSmsModal'))
  }
  ,
  closeViewAllSmsModal() {
    this.isViewAllSmsModalOpen = false
    this.trapCleanupViewAllSms()
  },


  // futsal match udpate modal
  isFutsalMatchUpdateModalOpen: false,
  trapCleanupFutsalMatchUpdate: null,
  openFutsalMatchUpdateModal() {
    SearchByFutsalDate()
    this.isFutsalMatchUpdateModalOpen = true
    this.trapCleanupFutsalMatchUpdate = focusTrap(document.querySelector('#FutsalMatchUpdateModal'))

  },
  closeFutsalMatchUpdateModal() {
    this.isFutsalMatchUpdateModalOpen = false
    this.trapCleanupFutsalMatchUpdate()
  },

  // cafeteria customer model
  isCafeteriaCustomerModalOpen: false,
  trapCleanupCafeteriaCustomer: null,
  openCafeteriaCustomerModal() {
    this.isCafeteriaCustomerModalOpen = true
    this.trapCleanupCafeteriaCustomer = focusTrap(document.querySelector('#CafeteriaCustomerModal'))

  },
  closeCafeteriaCustomerModal() {
    this.isCafeteriaCustomerModalOpen = false
    this.trapCleanupCafeteriaCustomer()
  },

  // cafeteria History model
  isCafeteriaHistoryModalOpen: false,
  trapCleanupCafeteriaHistory: null,
  openCafeteriaHistoryModal() {
    this.isCafeteriaHistoryModalOpen = true
    this.trapCleanupCafeteriaHistory = focusTrap(document.querySelector('#CafeteriaHistoryModal'))

  },
  closeCafeteriaHistoryModal() {
    this.isCafeteriaHistoryModalOpen = false
    this.trapCleanupCafeteriaHistory()
  },

  // cafeteria  roder detail model
  // isCafeteriaOrderDetailModalOpen: false,
  // trapCleanupCafeteriaOrderDetail: null,
  // openCafeteriaOrderDetailModal(id) {
  //     this.isCafeteriaOrderDetailModalOpen = true
  //     this.trapCleanupCafeteriaOrderDetail = focusTrap(document.querySelector('#CafeteriaOrderDetailModal'))

  // },
  // closeCafeteriaHistoryModal() {
  //   this.isCafeteriaOrderDetailModalOpen = false
  //   this.trapCleanupCafeteriaOrderDetail()
  // },


  // cafeteria  print orderuf model
  isViewCafeteriaBillModalOpen: false,
  trapCleanupCafeteriaBillModel: null,
  openViewCafeteriaBillModal() {
    this.isViewCafeteriaBillModalOpen = true
    this.trapCleanupCafeteriaBillModel = focusTrap(document.querySelector('#ViewCafeteriaBillModal'))
    PrintTable();

  },
  closeCafeteriaBillModel() {
    this.isViewCafeteriaBillModalOpen = false
    this.trapCleanupCafeteriaBillModel()
  },


  // cafeteria  sales model
  isViewCafeteriaSalesModalOpen: false,
  trapCleanupCafeteriaSalesModel: null,
  openViewCafeteriaSalesModal() {
    this.isViewCafeteriaSalesModalOpen = true
    this.trapCleanupCafeteriaSalesModel = focusTrap(document.querySelector('#ViewCafeteriaSalesModal'))
    // PrintTable();

  },
  closeCafeteriaSalesModel() {
    this.isViewCafeteriaSalesModalOpen = false
    this.trapCleanupCafeteriaSalesModel()
  },

  // cafeteria  purchases return model
  isViewCafeteriaPurchasesModalOpen: false,
  trapCleanupCafeteriaPurchasesModel: null,
  openViewCafeteriaPurchasesModal(id) {
    this.isViewCafeteriaPurchasesModalOpen = true
    this.trapCleanupCafeteriaPurchasesModel = focusTrap(document.querySelector('#ViewCafeteriaPurchasesModal'))
    // PrintTable();
    LoadPurchaseReturn(id)

  },
  closeCafeteriaPurchasesModel() {
    this.isViewCafeteriaPurchasesModalOpen = false
    this.trapCleanupCafeteriaPurchasesModel()
  },


};


function data() {
  return window.alpine_data;
}

function ajax_call(id) {
  console.log("row id fetch ", id)
}