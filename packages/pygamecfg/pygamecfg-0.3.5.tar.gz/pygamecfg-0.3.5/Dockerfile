# pyChaChaDummyProject (c) by chacha
#
# pyChaChaDummyProject is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y python3.9 python3-virtualenv python3-pip git python3.9-venv weasyprint

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade virtualenv
RUN python3 -m pip install --upgrade setuptools wheel build