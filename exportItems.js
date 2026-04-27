(async () => {
  const dbName = "infinite-craft";
  const storeName = "items";

  function openDB(name) {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(name);

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  function getAllFromStore(db, store) {
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(store, "readonly");
      const objectStore = transaction.objectStore(store);
      const request = objectStore.getAll();

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  function downloadJSON(data, filename) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  try {
    const db = await openDB(dbName);

    if (!db.objectStoreNames.contains(storeName)) {
      throw new Error(`Object store "${storeName}" not found in IndexedDB "${dbName}".`);
    }

    const items = await getAllFromStore(db, storeName);

    downloadJSON(items, "infinite-craft-items.json");

    db.close();

    console.log(`Downloaded ${items.length} items from IndexedDB "${dbName}" / "${storeName}".`);
  } catch (error) {
    console.error("Failed to export IndexedDB items:", error);
  }
})();