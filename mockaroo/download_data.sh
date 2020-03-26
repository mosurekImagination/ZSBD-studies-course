#!/bin/bash

file_name=("Damage.sql" "Inspection.sql" "Invoice.sql" "Location.sql" "Payment.sql" "RentalHistory.sql" "StationWorker.sql" "SystemUser.sql" "Car.sql" "CarStation.sql" "Company.sql")
mock_id=("c3d97840" "067c9670" "daf08d40" "1baeae90" "f63b6dc0" "999f1150" "ffe78320" "53750680" "80d37bf0" "a1a9fd20" "f0cef740")
api_key=("ad682a30" "412852a0" "8f54b0b0" "ad682a30" "d1611e10" "412852a0" "8f54b0b0" "d1611e10" "412852a0" "8f54b0b0" "d1611e10")

for ((i=0; i<${#file_name[@]}; ++i)); do
    for j in {1..10};
      do
        echo "iteration ${j} - ${file_name[i]}"
        curl "https://api.mockaroo.com/api/${mock_id[i]}?count=5000&key=${api_key[i]}" >> "${file_name[i]}";
      done
done


