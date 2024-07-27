import os
import time
from datetime import datetime
from typing import List

import pandas as pd
import requests
from LivingInsider import LivingInsider

URLS: List[str] = [
    # "https://www.livinginsider.com/living_zone_en/18/Condo/Buysell/{page}/Sukhumvit-Asoke-Thonglor.html",
    # "https://www.livinginsider.com/living_zone_en/10/Condo/Buysell/{page}/Ladprao-Central-Ladprao.html",
    # "https://www.livinginsider.com/living_zone_en/14/Condo/Buysell/{page}/Rama9-RCA-Petchaburi.html",
    # "https://www.livinginsider.com/living_zone_en/24/Condo/Buysell/{page}/Sathorn-Narathiwat.html",
    "https://www.livinginsider.com/living_zone_en/26/Condo/Buysell/{page}/Wongwianyai-Charoennakor.html",
    "https://www.livinginsider.com/living_zone_en/13/Condo/Buysell/{page}/Ratchadapisek-Huaikwang-Suttisan.html",
    "https://www.livinginsider.com/living_zone_en/19/Condo/Buysell/{page}/Onnut-Udomsuk.html",
]
N_PAGES: int = 10
USE_CACHE: bool = False
OUTPUT_DIR: str = "/Users/avallerian/GitRepo/ConCoRd/ConCoRd"


def maybe_makedir(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f"directory created: {dir}")


def get_web_content(url: str) -> str:
    return requests.get(url).content


def main() -> None:
    curr_date: str = datetime.now().strftime("%Y%m%d")
    html_dir: str = f"{OUTPUT_DIR}/html/{curr_date}"
    result_dir: str = f"{OUTPUT_DIR}/result/{curr_date}"

    maybe_makedir(html_dir)
    maybe_makedir(result_dir)

    for url in URLS:
        for page in range(1, N_PAGES + 1):
            print(f"scraping url: {url.format(page=page)}")
            filename: str = url.rsplit("/", maxsplit=1)[-1].split(".")[0]

            if USE_CACHE:
                print(f"using cache from {html_dir}/{filename}_{page}.txt")
                with open(f"{html_dir}/{filename}_{page}.txt", "rb") as f:
                    content: str = f.read()
            else:
                content: str = get_web_content(url.format(page=page))
                with open(f"{html_dir}/{filename}_{page}.txt", "wb") as f:
                    f.write(content)

            ls: LivingInsider = LivingInsider(content=content)
            ls.extract()

            data: pd.DataFrame = pd.DataFrame(ls.condo_data)
            print(f"result: {len(data)} condo")
            data.to_csv(f"{result_dir}/{filename}_{page}.csv", index=0, quoting=1)
            print(f"save to csv: {result_dir}/{filename}_{page}.csv")

            time.sleep(5)

    print("done")


if __name__ == "__main__":
    main()
