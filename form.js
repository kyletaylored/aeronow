(function ($) {

    function getSites() {
        // Fetch data from API to store locally.
        var sites = localStorage.getItem("tceq_sites");
        if (sites == null) {
            try {
                sites = $.get("http://127.0.0.1:5000/api/sites", (data, status) => {
                    resp = JSON.parse(data);
                    console.log(resp);
                    localStorage.setItem("tceq_sites", data);
                });
            } catch (error) {
                console.error(error);
            }
        }
        sites = JSON.parse(sites)
        processZip(sites);
        return sites;
    }

    function processZip(sites) {
        var allZips = localStorage.getItem("tceq_zips");
        if (allZips == null) {
            // Store all zipcodes from sites
            var allZips = []
            sites.forEach((i, el) => {
                var zip = sites[el]['ZIP'];
                if ($.inArray(zip, allZips) === -1) {
                    allZips.push(zip);
                };
            });
            localStorage.setItem('tceq_zips', allZips.toString());
        }
    }
    
    function getZips() {
        var allZips = localStorage.getItem("tceq_zips");
        return allZips.split(",");
    }

    $(document).ready(function(){

        var sites = getSites();
        var zips = getZips();
        
        console.log(zips);

        var $form = $("#tceq_form");
        $form.on('submit', (event, val) => {
            event.preventDefault();
            var data = $form.serializeArray();
            var zipcode = ""
            data.forEach((el) => {
                if (el.name == 'zipcode') {
                    zipcode = el.value;
                }
            })
            
            var part_zip = zipcode.slice(0,2);
            zipcodes = [];
            for (zip in zips) {
                reg = "/"+part_zip+"/g";
                if (zip.match(reg)) {
                    zipcodes.push(zip);
                }
            };

            console.log(zipcodes);
            
            // $.get({
            //     url: "https://www.zipcodeapi.com/rest/n6wyHR7crfH4BaLFqJwxDkdH0sd1jxZxa49Sb4gvpnzbbDRrpkAuuW1HA3BHnmic/match-close.json/"+zipcodes+"/25/mile"
            // })

        })

    })

}(jQuery));